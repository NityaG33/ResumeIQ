# from auth.jwt import create_access_token, decode_access_token

# user_id = "user123"

# token = create_access_token({
#     "sub": user_id
# })

# print("JWT:")
# print(token)

# print("\nDecoded payload:")

# payload = decode_access_token(token)

# print(payload)




# Invalid Token test
# from auth.jwt import decode_access_token


# fake_token = "this-is-not-a-valid-jwt"

# payload = decode_access_token(fake_token)

# print(payload)


# Invalid Token test with expired token
# from datetime import timedelta
# import time
# from auth.jwt import create_access_token, decode_access_token


# token = create_access_token(
#     {"sub": "user123"},
#     expires_delta=timedelta(seconds=1)
# )

# print("Token created.")

# time.sleep(2)

# payload = decode_access_token(token)

# print(payload)