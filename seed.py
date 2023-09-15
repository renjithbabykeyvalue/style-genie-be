from mongoengine import *
from src.models.models import User, UserProfile, Designer, Fabric, Outfit, UserMeasurement, DefaultOption, CustomisedOption, Order
from datetime import datetime  # Import datetime module


def seed_database():
    # Create 5 User records with fixed data
    users = []
    for i in range(1, 6):
        user = User(
            email=f"user{i}@example.com",
            firstName=f"First{i}",
            lastName=f"Last{i}",
            dob=datetime(1990 + i, 1, 1)
        )
        user.save()
        users.append(user)

    # Create 5 UserProfile records with fixed data
    user_profiles = []
    for user in users:
        user_profile = UserProfile(
            nickname=f"Nickname-{user.id}",
            gender="Male",  # Replace with actual gender
            user=user
        )
        user_profile.save()
        user_profiles.append(user_profile)

    # Create 5 Designer records with fixed data
    designers = []
    for i in range(1, 6):
        designer = Designer(
            name=f"Designer{i}",
            email=f"designer{i}@example.com",
            phoneNumber=f"+123456789{i}",
            location=f"Location {i}"
        )
        designer.save()
        designers.append(designer)

    # Create 5 Fabric records with fixed data
    fabrics = []
    for i in range(1, 6):
        fabric = Fabric(
            name=f"Fabric{i}",
            designer=designers[i - 1],
            image_url=f"https://example.com/fabric{i}.jpg",
            price_per_meter=20 + i  # Adjust the price as needed
        )
        fabric.save()
        fabrics.append(fabric)

    # Create 5 Outfit records with fixed data
    outfits = []
    for i in range(1, 6):
        outfit = Outfit(
            name=f"Outfit{i}",
            designer=designers[i - 1],
            image_url=f"https://example.com/outfit{i}.jpg",
            default_price=100 + i,  # Adjust the price as needed
            category=f"Category-{i}"
        )
        outfit.save()
        outfits.append(outfit)

    # Create 5 UserMeasurement records with fixed data
    user_measurements = []
    for user_profile in user_profiles:
        user_measurement = UserMeasurement(
            chestSize="M",  # Replace with actual size
            userProfile=user_profile,
            waistSize="L",  # Replace with actual size
            hipSize="XL",   # Replace with actual size
            inseamLength="Regular"  # Replace with actual length
        )
        user_measurement.save()
        user_measurements.append(user_measurement)

    # Create 5 DefaultOption records with fixed data
    default_options = []
    for i in range(1, 6):
        default_option = DefaultOption(
            outfit=outfits[i - 1],
            fabric=fabrics[i - 1],
            neckPattern=f"Pattern-{i}",
            sleevePattern=f"Sleeve-{i}"
        )
        default_option.save()
        default_options.append(default_option)

    # Create 5 CustomisedOption records with fixed data
    customised_options = []
    for i in range(1, 6):
        customised_option = CustomisedOption(
            userProfile=user_profiles[i - 1],
            outfit=outfits[i - 1],
            fabric=fabrics[i - 1],
            neckPattern=f"Pattern-{i}",
            sleevePattern=f"Sleeve-{i}"
        )
        customised_option.save()
        customised_options.append(customised_option)

    # Create 5 Order records with fixed data
    orders = []
    for i in range(1, 6):
        order = Order(
            user=users[i - 1],
            UserProfile=user_profiles[i - 1],
            outfit=outfits[i - 1],
            customisedOption=customised_options[i - 1],
            totalPrice=str(150 + i * 10),  # Adjust the price as needed
            status="Pending"  # Replace with actual status
        )
        order.save()
        orders.append(order)


if __name__ == "__main__":
    seed_database()
