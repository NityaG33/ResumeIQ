from auth.service import create_user


email = "test1@example.com"
password = "hello123"

try:
    user = create_user(email, password)

    print("User created:")
    print(user)

except ValueError as e:
    print("Error:", e)