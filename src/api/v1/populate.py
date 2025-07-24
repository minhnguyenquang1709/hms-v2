from faker import Faker
faker = Faker("vi_VN")

street_names = ["Nguyễn Trãi", "Lê Lợi", "Trần Hưng Đạo", "Phan Đình Phùng"]
city_names = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ", "Nha Trang", "Huế", "Vũng Tàu", "Biên Hòa", "Bắc Ninh", "Hải Phòng"]
for _ in range(10):
  print(f"{faker.building_number()} {faker.random.choice(street_names)}, {faker.random.choice(city_names)}")