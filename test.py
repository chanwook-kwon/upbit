import pyupbit
access = "8BVxcVc5ahBZv6bnT4vGS5cfoaY7bDoxso8CFcD8"
secret = "XS3k2r64b5LxxoNN4dsAxxGxEtWPgLJVKy0CyI05"
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XEC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회