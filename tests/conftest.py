import os


# Use a separate MongoDB database for automated tests
os.environ["DATABASE_NAME"] = "resumeiq_test"