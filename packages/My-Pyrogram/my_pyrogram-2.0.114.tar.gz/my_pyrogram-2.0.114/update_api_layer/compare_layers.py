def main():
    with open('./old_api.tl', mode='rt') as file:
        old_lines = get_lines(file.read())

    with open('./new_api.tl', mode='rt') as file:
        new_lines = get_lines(file.read())
    old_names = [parse_line(line) for line in old_lines]
    new_names = [parse_line(line) for line in new_lines]
    print('old_names', len(old_names))
    print('new_names', len(new_names))
    old_different_names = [name for name in old_names if name not in new_names]
    new_different_names = [name for name in new_names if name not in old_names]
    print('new_different_names', len(new_different_names))
    print('old_different_names', len(old_different_names))
    for name in old_different_names:
        if name in (
            'updateBroadcastRevenueTransactions', 'inputStorePaymentStars', 'premiumGiftOption',
            'stats.broadcastRevenueStats', 'stats.broadcastRevenueWithdrawalUrl',
            'broadcastRevenueTransactionProceeds', 'broadcastRevenueTransactionWithdrawal',
            'broadcastRevenueTransactionRefund', 'stats.broadcastRevenueTransactions',
            'broadcastRevenueBalances', 'users.getIsPremiumRequiredToContact',
            'channels.viewSponsoredMessage', 'channels.getSponsoredMessages',
            'channels.clickSponsoredMessage', 'channels.reportSponsoredMessage',
            'payments.canPurchasePremium', 'stats.getBroadcastRevenueStats',
            'stats.getBroadcastRevenueWithdrawalUrl', 'stats.getBroadcastRevenueTransactions',
            'emojiStatusUntil',
        ):
            continue
        print(name)


def get_lines(text: str) -> list[str]:
    lines = text.splitlines()
    return [
        line for line in [l.strip() for l in lines]
        if not line.startswith('//')
           and not line.startswith('---')
           and len(line) != 0
    ]

def parse_line(line: str) -> str:
    assert '#' in line
    name, _ = line.split('#', 1)
    assert len(name) != 0
    return name


if __name__ == '__main__':
    main()
