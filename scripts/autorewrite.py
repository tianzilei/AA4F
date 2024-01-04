# load text
import os
wkdir = os.getcwd()

# charaster replacement
import Faker
fake = Faker("zh_CN")
print(fake.name())