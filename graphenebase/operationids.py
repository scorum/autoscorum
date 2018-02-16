op_names = [
    'vote',
    'comment',
    'transfer',
    'transfer_to_vesting',
    'withdraw_vesting',
    'account_create_by_committee',
    'account_create',
    'account_create_with_delegation_operation',
    'account_update',
    'witness_update',
    'account_witness_vote',
    'account_witness_proxy',
    'pow',
    'custom',
    'report_over_production',
    'delete_comment',
    'custom_json',
    'comment_options',
    'set_withdraw_vesting_route',
    'limit_order_create2',
    'challenge_authority',
    'prove_authority',
    'request_account_recovery',
    'recover_account',
    'change_recovery_account',
    'escrow_transfer',
    'escrow_dispute',
    'escrow_release',
    'pow2',
    'escrow_approve',
    'transfer_to_savings',
    'transfer_from_savings',
    'cancel_transfer_from_savings',
    'custom_binary',
    'decline_voting_rights',
    'reset_account',
    'set_reset_account',
    'claim_reward_balance',
    'delegate_vesting_shares',
    'account_create_with_delegation',
    'fill_convert_request',
    'author_reward',
    'curation_reward',
    'comment_reward',
    'liquidity_reward',
    'interest',
    'fill_vesting_withdraw',
    'fill_order',
    'shutdown_witness',
    'fill_transfer_from_savings',
    'hardfork',
    'comment_payout_update',
    'return_vesting_delegation',
    'comment_benefactor_reward',
    'create_budget',
    'proposal_create'
]

#: assign operation ids
operations = dict(zip(op_names, range(len(op_names))))