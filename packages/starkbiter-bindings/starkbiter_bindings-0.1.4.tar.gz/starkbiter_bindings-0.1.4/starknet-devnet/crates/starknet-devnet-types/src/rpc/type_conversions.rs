use std::sync::Arc;

use cairo_lang_starknet_classes::contract_class::{
    ContractClass as SierraContractClass, ContractEntryPoint, ContractEntryPoints,
};
use cairo_lang_utils::bigint::BigUintAsHex;

use starknet_rs_core::types::{self as imported};

use crate::rpc::transactions::{
    BroadcastedTransactionCommonV3, l1_handler_transaction::L1HandlerTransaction,
};

use super::block::{Block, PendingBlock, ResourcePrice};
use super::contract_address::ContractAddress;
use super::emitted_event::{EmittedEvent, Event, OrderedEvent};
use super::estimate_message_fee::FeeEstimateWrapper;
use super::messaging::{MessageToL1, OrderedMessageToL1};
use super::state::{
    ClassHashPair, ContractNonce, DeployedContract, ReplacedClasses, StateUpdateResult,
    StorageDiff, StorageEntry, ThinStateDiff,
};
use super::transaction_receipt::{ExecutionResources, FeeInUnits, TransactionReceipt};
use super::transactions::broadcasted_declare_transaction_v3::BroadcastedDeclareTransactionV3;
use super::transactions::broadcasted_deploy_account_transaction_v3::BroadcastedDeployAccountTransactionV3;
use super::transactions::broadcasted_invoke_transaction_v3::BroadcastedInvokeTransactionV3;

use super::transactions::{
    BlockTransactionTrace, BroadcastedDeclareTransaction, BroadcastedDeployAccountTransaction,
    BroadcastedInvokeTransaction, BroadcastedTransaction, CallType, DeclareTransaction,
    DeployAccountTransaction, ExecutionInvocation, FunctionInvocation, InnerExecutionResources,
    InvokeTransaction, L1HandlerTransactionStatus, ResourceBoundsWrapper, Reversion,
    SimulatedTransaction, SimulationFlag, Transaction, TransactionStatus, TransactionTrace,
    TransactionWithHash, Transactions,
};

//
// Part 1.
//
// Conversions between devnet-core types and starknet-rs core types
// mostly from starknet-rs to starknet-devnet-types
//
// TODO: add backward conversions for all that are missing.
//

impl Into<Vec<imported::Felt>> for Transactions {
    fn into(self) -> Vec<imported::Felt> {
        match self {
            Transactions::Hashes(hashes) => hashes,
            Transactions::Full(txs) => {
                txs.iter().map(|tx| tx.get_transaction_hash()).map(|hash| *hash).collect()
            }
            Transactions::FullWithReceipts(txs) => txs
                .into_iter()
                .map(|tx_with_receipt| tx_with_receipt.receipt)
                .map(|receipt| match receipt {
                    TransactionReceipt::Deploy(receipt) => receipt.common,
                    TransactionReceipt::L1Handler(receipt) => receipt.common,
                    TransactionReceipt::Common(receipt) => receipt,
                })
                .map(|receipt| receipt.transaction_hash)
                .collect(),
        }
    }
}

impl From<TransactionWithHash> for imported::Transaction {
    fn from(tx_with_hash: TransactionWithHash) -> Self {
        let hash = *tx_with_hash.get_transaction_hash();
        match tx_with_hash.transaction {
            Transaction::Declare(DeclareTransaction::V3(tx)) => imported::Transaction::Declare(
                imported::DeclareTransaction::V3(imported::DeclareTransactionV3 {
                    transaction_hash: hash,
                    sender_address: tx.sender_address.into(),
                    compiled_class_hash: *tx.get_class_hash(),
                    signature: tx.signature,
                    nonce: tx.nonce,
                    class_hash: tx.class_hash,
                    resource_bounds: tx.resource_bounds.inner,
                    tip: tx.tip.0,
                    paymaster_data: tx.paymaster_data,
                    account_deployment_data: tx.account_deployment_data,
                    nonce_data_availability_mode: match tx.nonce_data_availability_mode {
                        starknet_api::data_availability::DataAvailabilityMode::L1 => {
                            imported::DataAvailabilityMode::L1
                        }
                        starknet_api::data_availability::DataAvailabilityMode::L2 => {
                            imported::DataAvailabilityMode::L2
                        }
                    },
                    fee_data_availability_mode: match tx.fee_data_availability_mode {
                        starknet_api::data_availability::DataAvailabilityMode::L1 => {
                            imported::DataAvailabilityMode::L1
                        }
                        starknet_api::data_availability::DataAvailabilityMode::L2 => {
                            imported::DataAvailabilityMode::L2
                        }
                    },
                }),
            ),
            Transaction::DeployAccount(DeployAccountTransaction::V3(tx)) => {
                imported::Transaction::DeployAccount(imported::DeployAccountTransaction::V3(
                    imported::DeployAccountTransactionV3 {
                        transaction_hash: hash,
                        signature: tx.signature,
                        nonce: tx.nonce,
                        contract_address_salt: tx.contract_address_salt,
                        constructor_calldata: tx.constructor_calldata,
                        class_hash: tx.class_hash,
                        resource_bounds: tx.resource_bounds.inner,
                        tip: tx.tip.0,
                        paymaster_data: tx.paymaster_data,
                        nonce_data_availability_mode: match tx.nonce_data_availability_mode {
                            starknet_api::data_availability::DataAvailabilityMode::L1 => {
                                imported::DataAvailabilityMode::L1
                            }
                            starknet_api::data_availability::DataAvailabilityMode::L2 => {
                                imported::DataAvailabilityMode::L2
                            }
                        },
                        fee_data_availability_mode: match tx.fee_data_availability_mode {
                            starknet_api::data_availability::DataAvailabilityMode::L1 => {
                                imported::DataAvailabilityMode::L1
                            }
                            starknet_api::data_availability::DataAvailabilityMode::L2 => {
                                imported::DataAvailabilityMode::L2
                            }
                        },
                    },
                ))
            }
            Transaction::Deploy(tx) => imported::Transaction::Deploy(imported::DeployTransaction {
                transaction_hash: hash,
                constructor_calldata: tx.constructor_calldata,
                class_hash: tx.class_hash,
                version: tx.version,
                contract_address_salt: tx.contract_address_salt,
            }),
            Transaction::Invoke(InvokeTransaction::V3(tx)) => imported::Transaction::Invoke(
                imported::InvokeTransaction::V3(imported::InvokeTransactionV3 {
                    transaction_hash: hash,
                    sender_address: tx.sender_address.into(),
                    calldata: tx.calldata,
                    signature: tx.signature,
                    nonce: tx.nonce,
                    resource_bounds: tx.resource_bounds.inner,
                    tip: tx.tip.0,
                    paymaster_data: tx.paymaster_data,
                    account_deployment_data: tx.account_deployment_data,
                    nonce_data_availability_mode: match tx.nonce_data_availability_mode {
                        starknet_api::data_availability::DataAvailabilityMode::L1 => {
                            imported::DataAvailabilityMode::L1
                        }
                        starknet_api::data_availability::DataAvailabilityMode::L2 => {
                            imported::DataAvailabilityMode::L2
                        }
                    },
                    fee_data_availability_mode: match tx.fee_data_availability_mode {
                        starknet_api::data_availability::DataAvailabilityMode::L1 => {
                            imported::DataAvailabilityMode::L1
                        }
                        starknet_api::data_availability::DataAvailabilityMode::L2 => {
                            imported::DataAvailabilityMode::L2
                        }
                    },
                }),
            ),
            Transaction::L1Handler(tx) => {
                imported::Transaction::L1Handler(imported::L1HandlerTransaction {
                    transaction_hash: hash,
                    version: tx.version,
                    nonce: tx.nonce.to_be_digits()[3], // TODO: check this
                    contract_address: tx.contract_address.into(),
                    entry_point_selector: tx.entry_point_selector,
                    calldata: tx.calldata,
                })
            }
        }
    }
}
impl Into<Vec<imported::Transaction>> for Transactions {
    fn into(self) -> Vec<imported::Transaction> {
        match self {
            Transactions::Hashes(_) => unimplemented!(),
            Transactions::Full(txs) => txs
                .iter()
                .map(|tx_with_hash| tx_with_hash)
                // TODO: warning clone!!!
                .cloned()
                .map(|tx| imported::Transaction::from(tx))
                .collect(),
            Transactions::FullWithReceipts(txs) => txs
                .into_iter()
                .map(|tx_with_receipt| {
                    TransactionWithHash::new(
                        match tx_with_receipt.receipt {
                            TransactionReceipt::Deploy(receipt) => receipt.common.transaction_hash,
                            TransactionReceipt::L1Handler(receipt) => {
                                receipt.common.transaction_hash
                            }
                            TransactionReceipt::Common(receipt) => receipt.transaction_hash,
                        },
                        tx_with_receipt.transaction,
                    )
                })
                .map(|tx_with_hash| imported::Transaction::from(tx_with_hash))
                .collect(),
        }
    }
}
impl From<Transaction> for imported::TransactionContent {
    fn from(value: Transaction) -> Self {
        match value {
            Transaction::Declare(DeclareTransaction::V3(tx)) => {
                imported::TransactionContent::Declare(imported::DeclareTransactionContent::V3(
                    imported::DeclareTransactionV3Content {
                        sender_address: tx.sender_address.into(),
                        compiled_class_hash: tx.compiled_class_hash,
                        signature: tx.signature,
                        nonce: tx.nonce,
                        class_hash: tx.class_hash,
                        resource_bounds: tx.resource_bounds.inner,
                        tip: tx.tip.0,
                        paymaster_data: tx.paymaster_data,
                        account_deployment_data: tx.account_deployment_data,
                        nonce_data_availability_mode: match tx.nonce_data_availability_mode {
                            starknet_api::data_availability::DataAvailabilityMode::L1 => {
                                imported::DataAvailabilityMode::L1
                            }
                            starknet_api::data_availability::DataAvailabilityMode::L2 => {
                                imported::DataAvailabilityMode::L2
                            }
                        },
                        fee_data_availability_mode: match tx.fee_data_availability_mode {
                            starknet_api::data_availability::DataAvailabilityMode::L1 => {
                                imported::DataAvailabilityMode::L1
                            }
                            starknet_api::data_availability::DataAvailabilityMode::L2 => {
                                imported::DataAvailabilityMode::L2
                            }
                        },
                    },
                ))
            }
            Transaction::DeployAccount(DeployAccountTransaction::V3(tx)) => {
                imported::TransactionContent::DeployAccount(
                    imported::DeployAccountTransactionContent::V3(
                        imported::DeployAccountTransactionV3Content {
                            signature: tx.signature,
                            nonce: tx.nonce,
                            contract_address_salt: tx.contract_address_salt,
                            constructor_calldata: tx.constructor_calldata,
                            class_hash: tx.class_hash,
                            resource_bounds: tx.resource_bounds.inner,
                            tip: tx.tip.0,
                            paymaster_data: tx.paymaster_data,

                            nonce_data_availability_mode: match tx.nonce_data_availability_mode {
                                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                                    imported::DataAvailabilityMode::L1
                                }
                                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                                    imported::DataAvailabilityMode::L2
                                }
                            },
                            fee_data_availability_mode: match tx.fee_data_availability_mode {
                                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                                    imported::DataAvailabilityMode::L1
                                }
                                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                                    imported::DataAvailabilityMode::L2
                                }
                            },
                        },
                    ),
                )
            }
            Transaction::Deploy(tx) => {
                imported::TransactionContent::Deploy(imported::DeployTransactionContent {
                    constructor_calldata: tx.constructor_calldata,
                    class_hash: tx.class_hash,
                    version: tx.version,
                    contract_address_salt: tx.contract_address_salt,
                })
            }
            Transaction::Invoke(InvokeTransaction::V3(tx)) => imported::TransactionContent::Invoke(
                imported::InvokeTransactionContent::V3(imported::InvokeTransactionV3Content {
                    sender_address: tx.sender_address.into(),
                    calldata: tx.calldata,
                    signature: tx.signature,
                    nonce: tx.nonce,
                    resource_bounds: tx.resource_bounds.inner,
                    tip: tx.tip.0,
                    paymaster_data: tx.paymaster_data,
                    account_deployment_data: tx.account_deployment_data,
                    nonce_data_availability_mode: match tx.nonce_data_availability_mode {
                        starknet_api::data_availability::DataAvailabilityMode::L1 => {
                            imported::DataAvailabilityMode::L1
                        }
                        starknet_api::data_availability::DataAvailabilityMode::L2 => {
                            imported::DataAvailabilityMode::L2
                        }
                    },
                    fee_data_availability_mode: match tx.fee_data_availability_mode {
                        starknet_api::data_availability::DataAvailabilityMode::L1 => {
                            imported::DataAvailabilityMode::L1
                        }
                        starknet_api::data_availability::DataAvailabilityMode::L2 => {
                            imported::DataAvailabilityMode::L2
                        }
                    },
                }),
            ),
            Transaction::L1Handler(tx) => {
                imported::TransactionContent::L1Handler(imported::L1HandlerTransactionContent {
                    version: tx.version,
                    nonce: tx.nonce.to_be_digits()[3], // TODO: check this
                    contract_address: tx.contract_address.into(),
                    entry_point_selector: tx.entry_point_selector,
                    calldata: tx.calldata,
                })
            }
        }
    }
}
impl Into<imported::FeePayment> for FeeInUnits {
    fn into(self) -> imported::FeePayment {
        match self {
            FeeInUnits::WEI(fee_amount) => imported::FeePayment {
                amount: fee_amount.amount.into(),
                unit: imported::PriceUnit::Wei,
            },
            FeeInUnits::FRI(fee_amount) => imported::FeePayment {
                amount: fee_amount.amount.into(),
                unit: imported::PriceUnit::Fri,
            },
        }
    }
}
impl Into<imported::MsgToL1> for MessageToL1 {
    fn into(self) -> imported::MsgToL1 {
        imported::MsgToL1 {
            from_address: self.from_address.into(),
            to_address: self.to_address.into(),
            payload: self.payload,
        }
    }
}
impl Into<imported::Event> for Event {
    fn into(self) -> imported::Event {
        imported::Event {
            from_address: self.from_address.0.to_felt(),
            keys: self.keys,
            data: self.data,
        }
    }
}

impl From<TransactionReceipt> for imported::TransactionReceipt {
    fn from(value: TransactionReceipt) -> Self {
        let common = match value.clone() {
            TransactionReceipt::Deploy(receipt) => receipt.common,
            TransactionReceipt::L1Handler(receipt) => receipt.common,
            TransactionReceipt::Common(receipt) => receipt,
        };

        match common.r#type {
            super::transactions::TransactionType::Declare => {
                imported::TransactionReceipt::Declare(imported::DeclareTransactionReceipt {
                    transaction_hash: common.transaction_hash,
                    actual_fee: common.actual_fee.into(),
                    finality_status: common.finality_status,
                    messages_sent: common.messages_sent.iter().cloned().map(Into::into).collect(),
                    events: common.events.iter().cloned().map(Into::into).collect(),
                    execution_resources: common.execution_resources.into(),
                    execution_result: common.execution_status,
                })
            }
            super::transactions::TransactionType::Deploy => {
                let contract_address = if let TransactionReceipt::Deploy(receipt) = value {
                    receipt.contract_address
                } else {
                    unreachable!("Expected Deploy receipt")
                };

                imported::TransactionReceipt::Deploy(imported::DeployTransactionReceipt {
                    transaction_hash: common.transaction_hash,
                    actual_fee: common.actual_fee.into(),
                    finality_status: common.finality_status,
                    messages_sent: common.messages_sent.iter().cloned().map(Into::into).collect(),
                    events: common.events.iter().cloned().map(Into::into).collect(),
                    execution_resources: common.execution_resources.into(),
                    execution_result: common.execution_status,
                    contract_address: contract_address.into(),
                })
            }
            super::transactions::TransactionType::DeployAccount => {
                let contract_address = if let TransactionReceipt::Deploy(receipt) = value {
                    receipt.contract_address
                } else {
                    unreachable!("Expected Deploy receipt")
                };

                imported::TransactionReceipt::DeployAccount(
                    imported::DeployAccountTransactionReceipt {
                        transaction_hash: common.transaction_hash,
                        actual_fee: common.actual_fee.into(),
                        finality_status: common.finality_status,
                        messages_sent: common
                            .messages_sent
                            .iter()
                            .cloned()
                            .map(Into::into)
                            .collect(),
                        events: common.events.iter().cloned().map(Into::into).collect(),
                        execution_resources: common.execution_resources.into(),
                        execution_result: common.execution_status,
                        contract_address: contract_address.into(),
                    },
                )
            }
            super::transactions::TransactionType::Invoke => {
                imported::TransactionReceipt::Invoke(imported::InvokeTransactionReceipt {
                    transaction_hash: common.transaction_hash,
                    actual_fee: common.actual_fee.into(),
                    finality_status: common.finality_status,
                    messages_sent: common.messages_sent.iter().cloned().map(Into::into).collect(),
                    events: common.events.iter().cloned().map(Into::into).collect(),
                    execution_resources: common.execution_resources.into(),
                    execution_result: common.execution_status,
                })
            }
            super::transactions::TransactionType::L1Handler => {
                let message_hash = if let TransactionReceipt::L1Handler(receipt) = value {
                    receipt.message_hash
                } else {
                    unreachable!("Expected Deploy receipt")
                };

                imported::TransactionReceipt::L1Handler(imported::L1HandlerTransactionReceipt {
                    transaction_hash: common.transaction_hash,
                    actual_fee: common.actual_fee.into(),
                    finality_status: common.finality_status,
                    messages_sent: common.messages_sent.iter().cloned().map(Into::into).collect(),
                    events: common.events.iter().cloned().map(Into::into).collect(),
                    execution_resources: common.execution_resources.into(),
                    execution_result: common.execution_status,
                    message_hash,
                })
            }
        }
    }
}
impl From<Transactions> for Vec<imported::TransactionWithReceipt> {
    fn from(value: Transactions) -> Self {
        match value {
            Transactions::Hashes(_) => unimplemented!(),
            Transactions::Full(_) => unimplemented!(),
            Transactions::FullWithReceipts(txs_with_receipt) => txs_with_receipt
                .iter()
                .map(|tx| imported::TransactionWithReceipt {
                    transaction: imported::TransactionContent::from(tx.transaction.clone()),
                    receipt: imported::TransactionReceipt::from(tx.receipt.clone()),
                })
                .collect(),
        }
    }
}

impl From<&L1HandlerTransactionStatus> for imported::MessageWithStatus {
    fn from(value: &L1HandlerTransactionStatus) -> Self {
        let message_status = if let Some(reason) = value.failure_reason.clone() {
            imported::MessageStatus::Rejected { reason }
        } else {
            match value.finality_status {
                imported::TransactionFinalityStatus::AcceptedOnL2 => {
                    imported::MessageStatus::AcceptedOnL2
                }
                imported::TransactionFinalityStatus::AcceptedOnL1 => {
                    imported::MessageStatus::AcceptedOnL1
                }
            }
        };

        return imported::MessageWithStatus {
            transaction_hash: value.transaction_hash,
            status: message_status,
        };
    }
}

impl From<Block> for imported::BlockWithReceipts {
    fn from(value: Block) -> Self {
        Self {
            transactions: value.transactions.into(),
            parent_hash: value.header.parent_hash,
            timestamp: value.header.timestamp.0,
            sequencer_address: value.header.sequencer_address.into(),
            l1_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_gas_price.price_in_fri,
                price_in_wei: value.header.l1_gas_price.price_in_wei,
            },
            l2_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l2_gas_price.price_in_fri,
                price_in_wei: value.header.l2_gas_price.price_in_wei,
            },
            l1_data_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_data_gas_price.price_in_fri,
                price_in_wei: value.header.l1_data_gas_price.price_in_wei,
            },
            l1_da_mode: match value.header.l1_da_mode {
                starknet_api::data_availability::L1DataAvailabilityMode::Blob => {
                    imported::L1DataAvailabilityMode::Blob
                }
                starknet_api::data_availability::L1DataAvailabilityMode::Calldata => {
                    imported::L1DataAvailabilityMode::Calldata
                }
            },
            starknet_version: value.header.starknet_version,
            status: match value.status {
                starknet_api::block::BlockStatus::Pending => imported::BlockStatus::Pending,
                starknet_api::block::BlockStatus::AcceptedOnL2 => {
                    imported::BlockStatus::AcceptedOnL2
                }
                starknet_api::block::BlockStatus::AcceptedOnL1 => {
                    imported::BlockStatus::AcceptedOnL1
                }
                starknet_api::block::BlockStatus::Rejected => imported::BlockStatus::Rejected,
            },
            block_hash: value.header.block_hash,
            block_number: value.header.block_number.0,
            new_root: value.header.new_root,
        }
    }
}
impl From<PendingBlock> for imported::PendingBlockWithReceipts {
    fn from(value: PendingBlock) -> Self {
        Self {
            transactions: value.transactions.into(),
            parent_hash: value.header.parent_hash,
            timestamp: value.header.timestamp.0,
            sequencer_address: value.header.sequencer_address.into(),
            l1_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_gas_price.price_in_fri,
                price_in_wei: value.header.l1_gas_price.price_in_wei,
            },
            l2_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l2_gas_price.price_in_fri,
                price_in_wei: value.header.l2_gas_price.price_in_wei,
            },
            l1_data_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_data_gas_price.price_in_fri,
                price_in_wei: value.header.l1_data_gas_price.price_in_wei,
            },
            l1_da_mode: match value.header.l1_da_mode {
                starknet_api::data_availability::L1DataAvailabilityMode::Blob => {
                    imported::L1DataAvailabilityMode::Blob
                }
                starknet_api::data_availability::L1DataAvailabilityMode::Calldata => {
                    imported::L1DataAvailabilityMode::Calldata
                }
            },
            starknet_version: value.header.starknet_version,
        }
    }
}

impl From<Block> for imported::BlockWithTxs {
    fn from(value: Block) -> Self {
        Self {
            transactions: value.transactions.into(),
            parent_hash: value.header.parent_hash,
            timestamp: value.header.timestamp.0,
            sequencer_address: value.header.sequencer_address.into(),
            l1_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_gas_price.price_in_fri,
                price_in_wei: value.header.l1_gas_price.price_in_wei,
            },
            l2_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l2_gas_price.price_in_fri,
                price_in_wei: value.header.l2_gas_price.price_in_wei,
            },
            l1_data_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_data_gas_price.price_in_fri,
                price_in_wei: value.header.l1_data_gas_price.price_in_wei,
            },
            l1_da_mode: match value.header.l1_da_mode {
                starknet_api::data_availability::L1DataAvailabilityMode::Blob => {
                    imported::L1DataAvailabilityMode::Blob
                }
                starknet_api::data_availability::L1DataAvailabilityMode::Calldata => {
                    imported::L1DataAvailabilityMode::Calldata
                }
            },
            starknet_version: value.header.starknet_version,
            status: match value.status {
                starknet_api::block::BlockStatus::Pending => imported::BlockStatus::Pending,
                starknet_api::block::BlockStatus::AcceptedOnL2 => {
                    imported::BlockStatus::AcceptedOnL2
                }
                starknet_api::block::BlockStatus::AcceptedOnL1 => {
                    imported::BlockStatus::AcceptedOnL1
                }
                starknet_api::block::BlockStatus::Rejected => imported::BlockStatus::Rejected,
            },
            block_hash: value.header.block_hash,
            block_number: value.header.block_number.0,
            new_root: value.header.new_root,
        }
    }
}
impl From<PendingBlock> for imported::PendingBlockWithTxs {
    fn from(value: PendingBlock) -> Self {
        Self {
            transactions: value.transactions.into(),
            parent_hash: value.header.parent_hash,
            timestamp: value.header.timestamp.0,
            sequencer_address: value.header.sequencer_address.into(),
            l1_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_gas_price.price_in_fri,
                price_in_wei: value.header.l1_gas_price.price_in_wei,
            },
            l2_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l2_gas_price.price_in_fri,
                price_in_wei: value.header.l2_gas_price.price_in_wei,
            },
            l1_data_gas_price: imported::ResourcePrice {
                price_in_fri: value.header.l1_data_gas_price.price_in_fri,
                price_in_wei: value.header.l1_data_gas_price.price_in_wei,
            },
            l1_da_mode: match value.header.l1_da_mode {
                starknet_api::data_availability::L1DataAvailabilityMode::Blob => {
                    imported::L1DataAvailabilityMode::Blob
                }
                starknet_api::data_availability::L1DataAvailabilityMode::Calldata => {
                    imported::L1DataAvailabilityMode::Calldata
                }
            },
            starknet_version: value.header.starknet_version,
        }
    }
}

impl From<Block> for imported::BlockWithTxHashes {
    fn from(block: Block) -> Self {
        let hashes: Vec<imported::Felt> = block.transactions.into();

        Self {
            transactions: hashes,
            status: match block.status {
                starknet_api::block::BlockStatus::Pending => imported::BlockStatus::Pending,
                starknet_api::block::BlockStatus::AcceptedOnL2 => {
                    imported::BlockStatus::AcceptedOnL2
                }
                starknet_api::block::BlockStatus::AcceptedOnL1 => {
                    imported::BlockStatus::AcceptedOnL1
                }
                starknet_api::block::BlockStatus::Rejected => imported::BlockStatus::Rejected,
            },
            block_hash: block.header.block_hash,
            block_number: block.header.block_number.0,
            new_root: block.header.new_root,
            parent_hash: block.header.parent_hash,
            timestamp: block.header.timestamp.0,
            sequencer_address: block.header.sequencer_address.into(),
            l1_gas_price: block.header.l1_gas_price.into(),
            l2_gas_price: block.header.l2_gas_price.into(),
            l1_data_gas_price: block.header.l1_data_gas_price.into(),
            l1_da_mode: match block.header.l1_da_mode {
                starknet_api::data_availability::L1DataAvailabilityMode::Blob => {
                    imported::L1DataAvailabilityMode::Blob
                }
                starknet_api::data_availability::L1DataAvailabilityMode::Calldata => {
                    imported::L1DataAvailabilityMode::Calldata
                }
            },
            starknet_version: block.header.starknet_version,
        }
    }
}

impl From<ResourcePrice> for imported::ResourcePrice {
    fn from(value: ResourcePrice) -> Self {
        imported::ResourcePrice {
            price_in_fri: value.price_in_fri,
            price_in_wei: value.price_in_wei,
        }
    }
}

impl From<PendingBlock> for imported::PendingBlockWithTxHashes {
    fn from(block: PendingBlock) -> Self {
        let hashes: Vec<imported::Felt> = block.transactions.into();

        Self {
            transactions: hashes,
            parent_hash: block.header.parent_hash,
            timestamp: block.header.timestamp.0,
            sequencer_address: block.header.sequencer_address.into(),
            l1_gas_price: block.header.l1_gas_price.into(),
            l2_gas_price: block.header.l2_gas_price.into(),
            l1_data_gas_price: block.header.l1_data_gas_price.into(),
            l1_da_mode: match block.header.l1_da_mode {
                starknet_api::data_availability::L1DataAvailabilityMode::Blob => {
                    imported::L1DataAvailabilityMode::Blob
                }
                starknet_api::data_availability::L1DataAvailabilityMode::Calldata => {
                    imported::L1DataAvailabilityMode::Calldata
                }
            },
            starknet_version: block.header.starknet_version,
        }
    }
}

impl From<TransactionStatus> for imported::TransactionStatus {
    fn from(value: TransactionStatus) -> Self {
        let reason = value.failure_reason.unwrap_or("unknown".to_string());

        return match value.finality_status {
            imported::TransactionFinalityStatus::AcceptedOnL1 => {
                imported::TransactionStatus::AcceptedOnL1(match value.execution_status {
                    imported::TransactionExecutionStatus::Succeeded => {
                        imported::ExecutionResult::Succeeded
                    }
                    imported::TransactionExecutionStatus::Reverted => {
                        imported::ExecutionResult::Reverted { reason }
                    }
                })
            }
            imported::TransactionFinalityStatus::AcceptedOnL2 => {
                imported::TransactionStatus::AcceptedOnL2(match value.execution_status {
                    imported::TransactionExecutionStatus::Succeeded => {
                        imported::ExecutionResult::Succeeded
                    }
                    imported::TransactionExecutionStatus::Reverted => {
                        imported::ExecutionResult::Reverted { reason }
                    }
                })
            }
        };
    }
}

impl From<TransactionReceipt> for imported::TransactionReceiptWithBlockInfo {
    fn from(value: TransactionReceipt) -> Self {
        let common = match value.clone() {
            TransactionReceipt::Deploy(receipt) => receipt.common,
            TransactionReceipt::L1Handler(receipt) => receipt.common,
            TransactionReceipt::Common(receipt) => receipt,
        };

        let block = if common.maybe_pending_properties.block_hash.is_none() {
            imported::ReceiptBlock::Pending
        } else {
            imported::ReceiptBlock::Block {
                block_hash: common.maybe_pending_properties.block_hash.unwrap(),
                block_number: common.maybe_pending_properties.block_number.unwrap().0,
            }
        };

        Self { receipt: value.into(), block }
    }
}

impl From<imported::ResourceBoundsMapping> for ResourceBoundsWrapper {
    fn from(value: imported::ResourceBoundsMapping) -> Self {
        ResourceBoundsWrapper { inner: value }
    }
}

impl From<ResourceBoundsWrapper> for imported::ResourceBoundsMapping {
    fn from(value: ResourceBoundsWrapper) -> Self {
        value.inner
    }
}

impl From<imported::BroadcastedInvokeTransactionV3> for BroadcastedInvokeTransactionV3 {
    fn from(value: imported::BroadcastedInvokeTransactionV3) -> Self {
        BroadcastedInvokeTransactionV3 {
            common: super::transactions::BroadcastedTransactionCommonV3 {
                version: 3.into(),
                signature: value.signature,
                nonce: value.nonce,
                resource_bounds: value.resource_bounds.into(),
                tip: starknet_api::transaction::fields::Tip(value.tip),
                paymaster_data: value.paymaster_data,
                nonce_data_availability_mode: match value.nonce_data_availability_mode {
                    imported::DataAvailabilityMode::L1 => {
                        starknet_api::data_availability::DataAvailabilityMode::L1
                    }
                    imported::DataAvailabilityMode::L2 => {
                        starknet_api::data_availability::DataAvailabilityMode::L2
                    }
                },
                fee_data_availability_mode: match value.fee_data_availability_mode {
                    imported::DataAvailabilityMode::L1 => {
                        starknet_api::data_availability::DataAvailabilityMode::L1
                    }
                    imported::DataAvailabilityMode::L2 => {
                        starknet_api::data_availability::DataAvailabilityMode::L2
                    }
                },
            },
            sender_address: ContractAddress::new(value.sender_address).expect("Should always work"),
            calldata: value.calldata,
            account_deployment_data: value.account_deployment_data,
        }
    }
}

impl From<BroadcastedInvokeTransactionV3> for imported::BroadcastedInvokeTransactionV3 {
    fn from(value: BroadcastedInvokeTransactionV3) -> Self {
        imported::BroadcastedInvokeTransactionV3 {
            sender_address: value.sender_address.0.to_felt(),
            calldata: value.calldata,
            signature: value.common.signature.clone(),
            nonce: value.common.nonce,
            resource_bounds: value.common.resource_bounds.clone().into(),
            tip: value.common.tip.0,
            paymaster_data: value.common.paymaster_data.clone(),
            account_deployment_data: value.account_deployment_data,
            nonce_data_availability_mode: match value.common.nonce_data_availability_mode {
                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                    imported::DataAvailabilityMode::L1
                }
                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                    imported::DataAvailabilityMode::L2
                }
            },
            fee_data_availability_mode: match value.common.fee_data_availability_mode {
                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                    imported::DataAvailabilityMode::L1
                }
                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                    imported::DataAvailabilityMode::L2
                }
            },
            is_query: value.common.is_only_query(),
        }
    }
}

impl From<imported::BroadcastedDeclareTransactionV3> for BroadcastedDeclareTransactionV3 {
    fn from(value: imported::BroadcastedDeclareTransactionV3) -> Self {
        BroadcastedDeclareTransactionV3 {
            common: super::transactions::BroadcastedTransactionCommonV3 {
                version: 3.into(),
                signature: value.signature.clone(),
                nonce: value.nonce,
                resource_bounds: ResourceBoundsWrapper { inner: value.resource_bounds },
                tip: starknet_api::transaction::fields::Tip(value.tip),
                paymaster_data: value.paymaster_data.clone(),
                nonce_data_availability_mode: match value.nonce_data_availability_mode {
                    imported::DataAvailabilityMode::L1 => {
                        starknet_api::data_availability::DataAvailabilityMode::L1
                    }
                    imported::DataAvailabilityMode::L2 => {
                        starknet_api::data_availability::DataAvailabilityMode::L2
                    }
                },
                fee_data_availability_mode: match value.fee_data_availability_mode {
                    imported::DataAvailabilityMode::L1 => {
                        starknet_api::data_availability::DataAvailabilityMode::L1
                    }
                    imported::DataAvailabilityMode::L2 => {
                        starknet_api::data_availability::DataAvailabilityMode::L2
                    }
                },
            },
            sender_address: ContractAddress::new(value.sender_address).expect("Should always work"),
            account_deployment_data: value.account_deployment_data,
            contract_class: sierra_from_contract_class(value.contract_class),
            compiled_class_hash: value.compiled_class_hash,
        }
    }
}

impl From<BroadcastedDeclareTransactionV3> for imported::BroadcastedDeclareTransactionV3 {
    fn from(value: BroadcastedDeclareTransactionV3) -> Self {
        imported::BroadcastedDeclareTransactionV3 {
            sender_address: value.sender_address.into(),
            compiled_class_hash: value.compiled_class_hash,
            signature: value.common.signature.clone(),
            nonce: value.common.nonce,
            resource_bounds: value.common.resource_bounds.clone().into(),
            tip: value.common.tip.0,
            paymaster_data: value.common.paymaster_data.clone(),
            account_deployment_data: value.account_deployment_data,
            nonce_data_availability_mode: match value.common.nonce_data_availability_mode {
                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                    imported::DataAvailabilityMode::L1
                }
                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                    imported::DataAvailabilityMode::L2
                }
            },
            fee_data_availability_mode: match value.common.fee_data_availability_mode {
                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                    imported::DataAvailabilityMode::L1
                }
                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                    imported::DataAvailabilityMode::L2
                }
            },
            is_query: value.common.is_only_query(),
            contract_class: Arc::new(contract_class_from_sierra(value.contract_class)),
        }
    }
}

impl From<imported::BroadcastedDeployAccountTransactionV3>
    for BroadcastedDeployAccountTransactionV3
{
    fn from(value: imported::BroadcastedDeployAccountTransactionV3) -> Self {
        BroadcastedDeployAccountTransactionV3 {
            common: super::transactions::BroadcastedTransactionCommonV3 {
                version: 3.into(),
                signature: value.signature.clone(),
                nonce: value.nonce,
                resource_bounds: ResourceBoundsWrapper { inner: value.resource_bounds },
                tip: starknet_api::transaction::fields::Tip(value.tip),
                paymaster_data: value.paymaster_data.clone(),
                nonce_data_availability_mode: match value.nonce_data_availability_mode {
                    imported::DataAvailabilityMode::L1 => {
                        starknet_api::data_availability::DataAvailabilityMode::L1
                    }
                    imported::DataAvailabilityMode::L2 => {
                        starknet_api::data_availability::DataAvailabilityMode::L2
                    }
                },
                fee_data_availability_mode: match value.fee_data_availability_mode {
                    imported::DataAvailabilityMode::L1 => {
                        starknet_api::data_availability::DataAvailabilityMode::L1
                    }
                    imported::DataAvailabilityMode::L2 => {
                        starknet_api::data_availability::DataAvailabilityMode::L2
                    }
                },
            },
            contract_address_salt: value.contract_address_salt,
            constructor_calldata: value.constructor_calldata,
            class_hash: value.class_hash,
        }
    }
}

impl From<BroadcastedDeployAccountTransactionV3>
    for imported::BroadcastedDeployAccountTransactionV3
{
    fn from(value: BroadcastedDeployAccountTransactionV3) -> Self {
        imported::BroadcastedDeployAccountTransactionV3 {
            signature: value.common.signature.clone(),
            nonce: value.common.nonce,
            resource_bounds: value.common.resource_bounds.clone().into(),
            tip: value.common.tip.0,
            paymaster_data: value.common.paymaster_data.clone(),
            contract_address_salt: value.contract_address_salt,
            constructor_calldata: value.constructor_calldata,
            class_hash: value.class_hash,
            nonce_data_availability_mode: match value.common.nonce_data_availability_mode {
                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                    imported::DataAvailabilityMode::L1
                }
                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                    imported::DataAvailabilityMode::L2
                }
            },
            fee_data_availability_mode: match value.common.fee_data_availability_mode {
                starknet_api::data_availability::DataAvailabilityMode::L1 => {
                    imported::DataAvailabilityMode::L1
                }
                starknet_api::data_availability::DataAvailabilityMode::L2 => {
                    imported::DataAvailabilityMode::L2
                }
            },
            is_query: value.common.is_only_query(),
        }
    }
}

impl From<FunctionInvocation> for imported::FunctionInvocation {
    fn from(value: FunctionInvocation) -> Self {
        imported::FunctionInvocation {
            contract_address: value.contract_address.into(),
            entry_point_selector: value.entry_point_selector,
            calldata: value.calldata,
            caller_address: value.caller_address.into(),
            class_hash: value.class_hash,
            // NOTE: OMG! Ouch 3rd 3rd party library
            entry_point_type: match value.entry_point_type {
                starknet_api::contract_class::EntryPointType::Constructor => {
                    imported::EntryPointType::Constructor
                }
                starknet_api::contract_class::EntryPointType::External => {
                    imported::EntryPointType::External
                }
                starknet_api::contract_class::EntryPointType::L1Handler => {
                    imported::EntryPointType::L1Handler
                }
            },
            call_type: value.call_type.into(),
            result: value.result,
            calls: value.calls.iter().cloned().map(Into::into).collect(),
            events: value.events.iter().cloned().map(Into::into).collect(),
            messages: value.messages.iter().cloned().map(Into::into).collect(),
            execution_resources: value.execution_resources.into(),
            is_reverted: value.is_reverted,
        }
    }
}

impl From<CallType> for imported::CallType {
    fn from(value: CallType) -> Self {
        match value {
            CallType::Call => imported::CallType::Call,
            CallType::Delegate => imported::CallType::Delegate,
            CallType::LibraryCall => imported::CallType::LibraryCall,
        }
    }
}

impl From<OrderedEvent> for imported::OrderedEvent {
    fn from(value: OrderedEvent) -> Self {
        imported::OrderedEvent { order: value.order as u64, keys: value.keys, data: value.data }
    }
}

impl From<OrderedMessageToL1> for imported::OrderedMessage {
    fn from(value: OrderedMessageToL1) -> Self {
        imported::OrderedMessage {
            order: value.order as u64,
            from_address: value.message.from_address.into(),
            to_address: value.message.to_address.into(),
            payload: value.message.payload,
        }
    }
}

impl From<InnerExecutionResources> for imported::InnerCallExecutionResources {
    fn from(value: InnerExecutionResources) -> Self {
        imported::InnerCallExecutionResources { l1_gas: value.l1_gas, l2_gas: value.l2_gas }
    }
}

impl From<StorageEntry> for imported::StorageEntry {
    fn from(value: StorageEntry) -> Self {
        imported::StorageEntry { key: value.key.to_felt(), value: value.value }
    }
}

impl From<StorageDiff> for imported::ContractStorageDiffItem {
    fn from(value: StorageDiff) -> Self {
        imported::ContractStorageDiffItem {
            address: value.address.into(),
            storage_entries: value.storage_entries.iter().cloned().map(Into::into).collect(),
        }
    }
}

impl From<ClassHashPair> for imported::DeclaredClassItem {
    fn from(value: ClassHashPair) -> Self {
        imported::DeclaredClassItem {
            class_hash: value.class_hash,
            compiled_class_hash: value.compiled_class_hash,
        }
    }
}

impl From<DeployedContract> for imported::DeployedContractItem {
    fn from(value: DeployedContract) -> Self {
        imported::DeployedContractItem {
            address: value.address.into(),
            class_hash: value.class_hash,
        }
    }
}

impl From<ReplacedClasses> for imported::ReplacedClassItem {
    fn from(value: ReplacedClasses) -> Self {
        imported::ReplacedClassItem {
            contract_address: value.contract_address.0.to_felt(),
            class_hash: value.class_hash,
        }
    }
}

impl From<ContractNonce> for imported::NonceUpdate {
    fn from(value: ContractNonce) -> Self {
        imported::NonceUpdate {
            contract_address: value.contract_address.into(),
            nonce: value.nonce,
        }
    }
}

impl From<ThinStateDiff> for imported::StateDiff {
    fn from(value: ThinStateDiff) -> Self {
        imported::StateDiff {
            storage_diffs: value.storage_diffs.iter().cloned().map(Into::into).collect(),
            deprecated_declared_classes: value.deprecated_declared_classes,
            declared_classes: value.declared_classes.iter().cloned().map(Into::into).collect(),
            deployed_contracts: value.deployed_contracts.iter().cloned().map(Into::into).collect(),
            replaced_classes: value.replaced_classes.iter().cloned().map(Into::into).collect(),
            nonces: value.nonces.iter().cloned().map(Into::into).collect(),
        }
    }
}

impl From<ExecutionResources> for imported::ExecutionResources {
    fn from(value: ExecutionResources) -> Self {
        imported::ExecutionResources {
            l1_gas: value.l1_gas,
            l1_data_gas: value.l1_data_gas,
            l2_gas: value.l2_gas,
        }
    }
}

impl From<ExecutionInvocation> for imported::ExecuteInvocation {
    fn from(value: ExecutionInvocation) -> Self {
        match value {
            ExecutionInvocation::Succeeded(invocation) => {
                imported::ExecuteInvocation::Success(invocation.into())
            }
            ExecutionInvocation::Reverted(Reversion { revert_reason }) => {
                imported::ExecuteInvocation::Reverted(imported::RevertedInvocation {
                    revert_reason,
                })
            }
        }
    }
}

impl From<TransactionTrace> for imported::TransactionTrace {
    fn from(value: TransactionTrace) -> Self {
        match value {
            TransactionTrace::Invoke(trace) => {
                imported::TransactionTrace::Invoke(imported::InvokeTransactionTrace {
                    validate_invocation: trace.validate_invocation.map(Into::into),
                    execute_invocation: trace.execute_invocation.into(),
                    fee_transfer_invocation: trace.fee_transfer_invocation.map(Into::into),
                    state_diff: trace.state_diff.map(Into::into),
                    execution_resources: trace.execution_resources.into(),
                })
            }
            TransactionTrace::Declare(trace) => {
                imported::TransactionTrace::Declare(imported::DeclareTransactionTrace {
                    validate_invocation: trace.validate_invocation.map(Into::into),
                    fee_transfer_invocation: trace.fee_transfer_invocation.map(Into::into),
                    state_diff: trace.state_diff.map(Into::into),
                    execution_resources: trace.execution_resources.into(),
                })
            }
            TransactionTrace::DeployAccount(trace) => {
                imported::TransactionTrace::DeployAccount(imported::DeployAccountTransactionTrace {
                    validate_invocation: trace.validate_invocation.map(Into::into),
                    constructor_invocation: trace
                        .constructor_invocation
                        .map(Into::into)
                        .expect("Should always be present"),
                    fee_transfer_invocation: trace.fee_transfer_invocation.map(Into::into),
                    state_diff: trace.state_diff.map(Into::into),
                    execution_resources: trace.execution_resources.into(),
                })
            }
            TransactionTrace::L1Handler(trace) => {
                imported::TransactionTrace::L1Handler(imported::L1HandlerTransactionTrace {
                    function_invocation: trace.function_invocation.into(),
                    state_diff: trace.state_diff.map(Into::into),
                    execution_resources: trace.execution_resources.into(),
                })
            }
        }
    }
}

impl From<SimulationFlag> for imported::SimulationFlag {
    fn from(value: SimulationFlag) -> Self {
        match value {
            SimulationFlag::SkipFeeCharge => imported::SimulationFlag::SkipFeeCharge,
            SimulationFlag::SkipValidate => imported::SimulationFlag::SkipValidate,
        }
    }
}

impl From<imported::SimulationFlag> for SimulationFlag {
    fn from(value: imported::SimulationFlag) -> Self {
        match value {
            imported::SimulationFlag::SkipFeeCharge => SimulationFlag::SkipFeeCharge,
            imported::SimulationFlag::SkipValidate => SimulationFlag::SkipValidate,
        }
    }
}

impl From<FeeEstimateWrapper> for imported::FeeEstimate {
    fn from(value: FeeEstimateWrapper) -> Self {
        imported::FeeEstimate {
            l1_gas_consumed: value.l1_gas_consumed.try_into().unwrap(),
            l1_gas_price: value.l1_gas_price.try_into().unwrap(),
            l2_gas_consumed: value.l2_gas_consumed.try_into().unwrap(),
            l2_gas_price: value.l2_gas_price.try_into().unwrap(),
            l1_data_gas_consumed: value.l1_data_gas_consumed.try_into().unwrap(),
            l1_data_gas_price: value.l1_data_gas_price.try_into().unwrap(),
            overall_fee: value.overall_fee.try_into().unwrap(),
            unit: value.unit,
        }
    }
}

impl From<SimulatedTransaction> for imported::SimulatedTransaction {
    fn from(value: SimulatedTransaction) -> Self {
        imported::SimulatedTransaction {
            transaction_trace: value.transaction_trace.into(),
            fee_estimation: value.fee_estimation.into(),
        }
    }
}

impl From<BlockTransactionTrace> for imported::TransactionTraceWithHash {
    fn from(value: BlockTransactionTrace) -> Self {
        imported::TransactionTraceWithHash {
            transaction_hash: value.transaction_hash,
            trace_root: value.trace_root.into(),
        }
    }
}

impl From<BroadcastedTransaction> for imported::BroadcastedTransaction {
    fn from(value: BroadcastedTransaction) -> Self {
        match value {
            BroadcastedTransaction::Invoke(BroadcastedInvokeTransaction::V3(tx)) => {
                imported::BroadcastedTransaction::Invoke(
                    imported::BroadcastedInvokeTransactionV3::from(tx),
                )
            }
            BroadcastedTransaction::Declare(BroadcastedDeclareTransaction::V3(tx)) => {
                imported::BroadcastedTransaction::Declare(
                    imported::BroadcastedDeclareTransactionV3::from(*tx),
                )
            }
            BroadcastedTransaction::DeployAccount(BroadcastedDeployAccountTransaction::V3(tx)) => {
                imported::BroadcastedTransaction::DeployAccount(
                    imported::BroadcastedDeployAccountTransactionV3::from(tx),
                )
            }
        }
    }
}

impl From<imported::BroadcastedTransaction> for BroadcastedTransaction {
    fn from(value: imported::BroadcastedTransaction) -> Self {
        match value {
            imported::BroadcastedTransaction::Invoke(tx) => BroadcastedTransaction::Invoke(
                BroadcastedInvokeTransaction::V3(BroadcastedInvokeTransactionV3::from(tx)),
            ),
            imported::BroadcastedTransaction::Declare(tx) => {
                BroadcastedTransaction::Declare(BroadcastedDeclareTransaction::V3(Box::new(
                    BroadcastedDeclareTransactionV3::from(tx),
                )))
            }
            imported::BroadcastedTransaction::DeployAccount(tx) => {
                BroadcastedTransaction::DeployAccount(BroadcastedDeployAccountTransaction::V3(
                    BroadcastedDeployAccountTransactionV3::from(tx),
                ))
            }
        }
    }
}

pub fn sierra_from_contract_class(
    contract_class: Arc<imported::FlattenedSierraClass>,
) -> SierraContractClass {
    SierraContractClass {
        sierra_program: contract_class
            .sierra_program
            .iter()
            .map(|el| el.to_biguint())
            .map(|el| BigUintAsHex { value: el })
            .collect(),
        sierra_program_debug_info: Option::None,
        contract_class_version: contract_class.contract_class_version.clone(),
        entry_points_by_type: ContractEntryPoints {
            external: contract_class
                .entry_points_by_type
                .external
                .iter()
                .map(|el| ContractEntryPoint {
                    selector: el.selector.to_biguint(),
                    function_idx: el.function_idx as usize,
                })
                .collect(),
            l1_handler: contract_class
                .entry_points_by_type
                .l1_handler
                .iter()
                .map(|el| ContractEntryPoint {
                    selector: el.selector.to_biguint(),
                    function_idx: el.function_idx as usize,
                })
                .collect(),
            constructor: contract_class
                .entry_points_by_type
                .constructor
                .iter()
                .map(|el| ContractEntryPoint {
                    selector: el.selector.to_biguint(),
                    function_idx: el.function_idx as usize,
                })
                .collect(),
        },
        abi: match serde_json::from_str(contract_class.abi.as_str()) {
            Ok(abi) => Some(abi),
            Err(_) => None,
        },
    }
}

pub fn contract_class_from_sierra(
    contract_class: SierraContractClass,
) -> imported::FlattenedSierraClass {
    imported::FlattenedSierraClass {
        sierra_program: contract_class
            .sierra_program
            .iter()
            .cloned()
            .map(|i| {
                i.value.try_into().expect("Bigint should fit Felt. Otherwise Sierra is broken")
            })
            .collect(),
        contract_class_version: contract_class.contract_class_version,
        entry_points_by_type: imported::EntryPointsByType {
            constructor: contract_class
                .entry_points_by_type
                .constructor
                .iter()
                .cloned()
                .map(|el| imported::SierraEntryPoint {
                    selector: el.selector.into(),
                    function_idx: el.function_idx as u64,
                })
                .collect(),
            external: contract_class
                .entry_points_by_type
                .external
                .iter()
                .cloned()
                .map(|el| imported::SierraEntryPoint {
                    selector: el.selector.into(),
                    function_idx: el.function_idx as u64,
                })
                .collect(),
            l1_handler: contract_class
                .entry_points_by_type
                .l1_handler
                .iter()
                .cloned()
                .map(|el| imported::SierraEntryPoint {
                    selector: el.selector.into(),
                    function_idx: el.function_idx as u64,
                })
                .collect(),
        },
        abi: match contract_class.abi {
            Some(contract) => contract.json(),
            None => "[]".to_string(),
        },
    }
}

impl From<imported::SimulationFlagForEstimateFee> for SimulationFlag {
    fn from(value: imported::SimulationFlagForEstimateFee) -> Self {
        match value {
            imported::SimulationFlagForEstimateFee::SkipValidate => SimulationFlag::SkipValidate,
        }
    }
}

impl From<StateUpdateResult> for imported::MaybePendingStateUpdate {
    fn from(value: StateUpdateResult) -> Self {
        match value {
            StateUpdateResult::StateUpdate(state) => {
                imported::MaybePendingStateUpdate::Update(imported::StateUpdate {
                    block_hash: state.block_hash,
                    old_root: state.old_root,
                    new_root: state.new_root,
                    state_diff: state.state_diff.into(),
                })
            }
            StateUpdateResult::PendingStateUpdate(state) => {
                imported::MaybePendingStateUpdate::PendingUpdate(imported::PendingStateUpdate {
                    old_root: state.old_root,
                    state_diff: state.state_diff.into(),
                })
            }
        }
    }
}

impl From<EmittedEvent> for imported::EmittedEvent {
    fn from(value: EmittedEvent) -> Self {
        imported::EmittedEvent {
            transaction_hash: value.transaction_hash,
            block_hash: value.block_hash,
            block_number: value.block_number.map(|el| el.0),
            from_address: value.from_address.into(),
            keys: value.keys,
            data: value.data,
        }
    }
}

impl<'a> From<&'a EmittedEvent> for imported::EmittedEvent {
    fn from(value: &'a EmittedEvent) -> Self {
        imported::EmittedEvent {
            transaction_hash: value.transaction_hash,
            block_hash: value.block_hash,
            block_number: value.block_number.map(|el| el.0),
            from_address: value.from_address.into(),
            keys: value.keys.clone(),
            data: value.data.clone(),
        }
    }
}

impl From<&imported::L1HandlerTransaction> for L1HandlerTransaction {
    fn from(value: &imported::L1HandlerTransaction) -> Self {
        Self {
            l1_transaction_hash: Some(value.transaction_hash.into()),
            version: value.version,
            nonce: value.nonce.into(),
            contract_address: ContractAddress::new(value.contract_address).unwrap(),
            entry_point_selector: value.entry_point_selector,
            calldata: value.calldata.clone(),
            paid_fee_on_l1: 1, // This is a placeholder value, as the actual fee is not available in this type
        }
    }
}

//
// Part 2.
//
// Conversions between devnet-core types and starknet-api types
// mostly from starknet-rs to starknet-devnet-types. Only transactions. Needed for transaction hash calculations.
//
// TODO: add backward conversions for all that are missing.
//

impl From<starknet_api::transaction::fields::ValidResourceBounds> for ResourceBoundsWrapper {
    fn from(value: starknet_api::transaction::fields::ValidResourceBounds) -> Self {
        match value {
            starknet_api::transaction::fields::ValidResourceBounds::L1Gas(resource_bounds) => {
                ResourceBoundsWrapper {
                    inner: imported::ResourceBoundsMapping {
                        l1_gas: imported::ResourceBounds {
                            max_amount: resource_bounds.max_amount.0,
                            max_price_per_unit: resource_bounds.max_price_per_unit.0,
                        },
                        l1_data_gas: imported::ResourceBounds {
                            max_amount: 0, // No L1 data gas for this case
                            max_price_per_unit: 0,
                        },
                        l2_gas: imported::ResourceBounds {
                            max_amount: 0, // No L2 gas for this case
                            max_price_per_unit: 0,
                        },
                    },
                }
            }
            starknet_api::transaction::fields::ValidResourceBounds::AllResources(
                all_resource_bounds,
            ) => ResourceBoundsWrapper {
                inner: imported::ResourceBoundsMapping {
                    l1_gas: imported::ResourceBounds {
                        max_amount: all_resource_bounds.l1_gas.max_amount.0,
                        max_price_per_unit: all_resource_bounds.l1_gas.max_price_per_unit.0,
                    },
                    l1_data_gas: imported::ResourceBounds {
                        max_amount: all_resource_bounds.l1_data_gas.max_amount.0,
                        max_price_per_unit: all_resource_bounds.l1_data_gas.max_price_per_unit.0,
                    },
                    l2_gas: imported::ResourceBounds {
                        max_amount: all_resource_bounds.l2_gas.max_amount.0,
                        max_price_per_unit: all_resource_bounds.l2_gas.max_price_per_unit.0,
                    },
                },
            },
        }
    }
}

impl From<starknet_api::transaction::DeployAccountTransactionV3>
    for BroadcastedDeployAccountTransactionV3
{
    fn from(value: starknet_api::transaction::DeployAccountTransactionV3) -> Self {
        Self {
            common: BroadcastedTransactionCommonV3 {
                version: imported::Felt::THREE,
                signature: value.signature.0.to_vec(),
                nonce: imported::Felt::ZERO,
                resource_bounds: value.resource_bounds.into(),
                tip: value.tip,
                paymaster_data: value.paymaster_data.0.to_vec(),
                nonce_data_availability_mode: value.nonce_data_availability_mode,
                fee_data_availability_mode: value.fee_data_availability_mode,
            },
            contract_address_salt: value.contract_address_salt.0,
            constructor_calldata: value.constructor_calldata.0.to_vec(),
            class_hash: value.class_hash.0,
        }
    }
}

impl From<starknet_api::transaction::DeployAccountTransactionV3>
    for BroadcastedDeployAccountTransaction
{
    fn from(value: starknet_api::transaction::DeployAccountTransactionV3) -> Self {
        BroadcastedDeployAccountTransaction::V3(value.into())
    }
}

impl From<starknet_api::transaction::DeployAccountTransaction>
    for BroadcastedDeployAccountTransaction
{
    fn from(value: starknet_api::transaction::DeployAccountTransaction) -> Self {
        match value {
            starknet_api::transaction::DeployAccountTransaction::V1(tx) => {
                unimplemented!("Devnet does not support V1 Account Deployment")
            }
            starknet_api::transaction::DeployAccountTransaction::V3(tx) => tx.into(),
        }
    }
}

impl From<starknet_api::transaction::InvokeTransactionV3> for BroadcastedInvokeTransactionV3 {
    fn from(value: starknet_api::transaction::InvokeTransactionV3) -> Self {
        Self {
            common: BroadcastedTransactionCommonV3 {
                version: imported::Felt::THREE,
                signature: value.signature.0.to_vec(),
                nonce: value.nonce.0,
                resource_bounds: value.resource_bounds.into(),
                tip: value.tip,
                paymaster_data: value.paymaster_data.0.to_vec(),
                nonce_data_availability_mode: value.nonce_data_availability_mode,
                fee_data_availability_mode: value.fee_data_availability_mode,
            },
            sender_address: ContractAddress::new(*value.sender_address.0.key()).unwrap(),
            calldata: value.calldata.0.to_vec(),
            account_deployment_data: value.account_deployment_data.0.to_vec(),
        }
    }
}

impl From<starknet_api::transaction::InvokeTransactionV3> for BroadcastedInvokeTransaction {
    fn from(value: starknet_api::transaction::InvokeTransactionV3) -> Self {
        BroadcastedInvokeTransaction::V3(value.into())
    }
}
