from mongoengine import *
from src.models.models import User, UserProfile, Designer, Fabric, Outfit, UserMeasurement, DefaultOption, CustomisedOption, Order
from datetime import datetime  # Import datetime module


def seed_database():
    userOne = User(
        email="anagha123@gmail.com",
        firstName="Anagha",
        lastName="Suresh",
        dob=datetime(2000, 11, 26)
    )
    userOne.save()

    userTwo = User(
        email="swathi321@gmail.com",
        firstName="Sreedivya",
        lastName="Nambiar",
        dob=datetime(1997, 10, 18)
    )
    userTwo.save()

    user_profile1 = UserProfile(
        nickname="Anu",
        gender="Female",  # Replace with actual gender
        user=userOne
    )
    user_profile1.save()

    user_profile2 = UserProfile(
        nickname="Anju",
        gender="Female",  # Replace with actual gender
        user=userOne
    )
    user_profile2.save()

    user_profile3 = UserProfile(
        nickname="Sree",
        gender="Female",  # Replace with actual gender
        user=userTwo
    )
    user_profile3.save()

    user_profile4 = UserProfile(
        nickname="Divya",
        gender="Female",  # Replace with actual gender
        user=userTwo
    )
    user_profile4.save()

    # Create 5 Designer records with fixed data

    designer1 = Designer(
        name="Beena Kannan",
        email="beenakannan@gmail.com",
        phoneNumber="9867124576",
        location="Kochi"
    )
    designer1.save()

    designer2 = Designer(
        name=" Leona Augustine",
        email="leona12@gmail.com",
        phoneNumber="9056789238",
        location="Bangalore"
    )
    designer2.save()

    outfitMain = Outfit(
        name="Green Long Dress",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/6503e8fde40d7addb33a5c7f",
        default_price=1200,  # Adjust the price as needed
        category="dress",
        description="Green dress which is easy to customize, fits every occasion"
    )

    outfitMain.save()

    outfit1 = Outfit(
        name="Cultsport",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/cultsport.jpg",
        default_price=1200,  # Adjust the price as needed
        category="kurta",
        description="Coltsport Women's Rayon Round Neck Straight Kurti | 3/4 Sleeve"
    )
    outfit1.save()

    outfit2 = Outfit(
        name="Gosriki",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/gosriki.jpg",
        default_price=2500,  # Adjust the price as needed
        category="kurta",
        description="GoSriKi Women Kurta and Palazzo"
    )
    outfit2.save()

    outfit3 = Outfit(
        name="Angraka",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/angraka.jpg",
        default_price=2400,  # Adjust the price as needed
        category="kurta",
        description="Angraka Women's Cotton Regular Kurta"

    )
    outfit3.save()

    outfit4 = Outfit(
        name="Rytras",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/rytras.jpg",
        default_price=1500,  # Adjust the price as needed
        category="kurta",
        description="rytras Women's Rayon Printed Purple Nayra Cut Flared Kurta"
    )
    outfit4.save()

    outfit5 = Outfit(
        name="Pacify",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/pacify.jpg",
        default_price=1780,  # Adjust the price as needed
        category="kurta",
        description="PACIFY Plus Size White Embroidered Solid Print Cotton Blend Straight Kurta"
    )
    outfit5.save()

    outfit6 = Outfit(
        name="Shiv",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/shiv.jpg",
        default_price=1300,  # Adjust the price as needed
        category="kurta",
        description="Shiv Textiles Rayon Fabric Printed Round Neck Short Kurtis for Women Top Dresses Kurti for Ladies & Girls Kurtis"

    )
    outfit6.save()

    outfit7 = Outfit(
        name="Luktrima",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/luktrima.jpg",
        default_price=1280,  # Adjust the price as needed
        category="top",
        description="Luktrima V Neck Stylish Full Sleeve Casual Wear Tops for Women and Gril's Tops"
    )

    outfit7.save()

    outfit8 = Outfit(
        name="Dream Beauty",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/dreambeauty.jpg",
        default_price=780,  # Adjust the price as needed
        category="top",
        description="Dream Beauty Fashion Women's Bishop Puff Sleeves Square Neck Slim Top Polyester Blend (23 Inches)"
    )

    outfit8.save()

    outfit9 = Outfit(
        name="Max",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/max.jpg",
        default_price=340,  # Adjust the price as needed
        category="top",
        description="Max Women Textured Round Neck T-Shirt"

    )

    outfit9.save()

    outfit10 = Outfit(
        name="Cotland",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/cotland.jpg",
        default_price=680,  # Adjust the price as needed
        category="top",
        description="COTLAND Fashions Jaipuri Cotton Printed Strappy Top for Women"

    )

    outfit10.save()

    outfit11 = Outfit(
        name="Rasa",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/rasa.jpg",
        default_price=650,  # Adjust the price as needed
        category="top",
        description="studio rasa Women's Georgette Sequin Embroidered Yoke Kaftan for Festive Wedding Party"

    )

    outfit11.save()

    outfit12 = Outfit(
        name="Fab alley",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/faballey.jpg",
        default_price=200,  # Adjust the price as needed
        category="dress",
        description="FabAlley Women Dress"

    )

    outfit12.save()

    outfit13 = Outfit(
        name="Vaani",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/vaani.jpg",
        default_price=1300,  # Adjust the price as needed
        category="dress",
        description="Vaani Creation Women's Maxi Anarkali Semi stitched "

    )

    outfit13.save()

    outfit14 = Outfit(
        name="Choli",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/choli.jpg",
        default_price=3500,  # Adjust the price as needed
        category="ethnic_wear",
        description="Fashion Basket Women's Georgette Semi-stitched Lehenga Choli Set "

    )

    outfit14.save()

    outfit15 = Outfit(
        name="Indya",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/indya.jpg",
        default_price=4300,  # Adjust the price as needed
        category="ethnic_wear",
        description="Indya Embroidered Georgette Strappy Womens Regular Crop Top (ITP00834-P)"

    )

    outfit15.save()

    outfit16 = Outfit(
        name="Kotty",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/kotty.jpg",
        default_price=700,  # Adjust the price as needed
        category="bottom",
        description="KOTTY Women Regular Length Royal Blue Solid Trousers"

    )

    outfit16.save()

    outfit17 = Outfit(
        name="Trasa",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/trasa.jpg",
        default_price=900,  # Adjust the price as needed
        category="bottom",
        description="TRASA Ultra Soft Cotton Regular and Plus 6 Colour Palazzo Pants for Womens and Girls - Available Sizes : L,XL,2XL,3XL"

    )

    outfit17.save()

    outfit18 = Outfit(
        name="Hasan",
        designer=designer1,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/hasan.jpg",
        default_price=1000,  # Adjust the price as needed
        category="shirt",
        description="THASAN Enterprises Women and Girls White Cotton Blend Delta Fancy Women Formal Shirt | Shirts for Women Stylish Western | Women Shirts Stylish Shirt"

    )

    outfit18.save()

    outfit19 = Outfit(
        name="Funday",
        designer=designer2,
        image_url="https://style-genie.s3.ap-south-1.amazonaws.com/outfits/data_stylegenie/funday.jpg",
        default_price=1600,  # Adjust the price as needed
        category="shirt",
        description="FUNDAY FASHION Women Casual Denim Mandarin Shirt"

    )

    outfit19.save()


if __name__ == "__main__":
    seed_database()
