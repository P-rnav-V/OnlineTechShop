import os 
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import text
from datetime import datetime

if os.path.exists('items.db'):
    os.remove('items.db')
    print("Old database deleted.")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    description = db.Column(db.String(300))
    delivery_time = db.Column(db.String(100), default="")           
    environmental_impact = db.Column(db.String(100), default="")
    envImpactsValue = db.Column(db.Integer, default=5)

    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship('Item', back_populates='reviews')
    
with app.app_context():
    db.session.execute(text('DROP TABLE IF EXISTS item'))
    db.session.commit()

    db.create_all()

    item1 = Item(name="Iphone 21", price=999, image="Iphone_21.png", description="The new 'revolutionary' Iphone by Maple does not really change much from the last iphone but the camera is different and the processor is slighly better so guess thats a good enough reason to buy it. This masterpiece of a device uses the all 'new' and amazing M21 Bionic chip (The M stands for Maple because brand image is important to us). This device also comes with a 1000 MP back camera and a 995 MP front camera. This device has everything you could ever wish for in a phone. We at Maple are very honest :)", delivery_time="1-2 working days", environmental_impact="(LOW). We at Maple choose to be as environmental friendly as possible. We re-use materials from our previous devices to make newer devices.", envImpactsValue=3)
    item2 = Item(name="Laptop 2100S pro max ultra", price=2049, image="Laptop2100s.jpg", description="Our brand new Laptop from the S series, releasing with a VERY slim display and a digital keyboard. Specs: RenVidia ETX 9090, QyZen10 7070 V, 110 GB RAM, 90GB VRAM, 1000 Hz refresh rate. But yes again, the display / screen is easily the best part of the laptop. I mean, seriously, just look at the picture, how could you not want to buy such a nice looking laptop. ",  delivery_time="1-2 working days", environmental_impact="(MEDIUM). This is due to the use of several high tier technologies used to create the functionality of the device, however, this device uses very environment-friendly materials to construct the display.", envImpactsValue=6)
    item3 = Item(name="Brain Chip Series A20", price=95600, image="BrainChip.png", description="The brand new Brain chip which allows you to LITERALLY live in your dreams. By simply implementing this device into your head right before sleeping, you have the option to become completely concious when you dream. You can also fully control what happens in your dreams. This is great when your awake too, as you can be fully immersed into your imagination. You pretty much live in your mind. DEVICE IMPLEMENTATION DETAILS: No need for any medical support as this device was made to be very quick and easy to implement and remove from your head. A manual providing detailed information will be included in your packaging. Your Imagination. Your Control. Your Reality. Your BrainChip.",  delivery_time="7-8 working days", environmental_impact="(EXTREMELY HIGH). This device uses very rare materials and nano tech. It also makes use of an extremely amount of energy due to being linked to an immersive neural simulation. It also manipulates your brain cells which also consumes a lot of enegry.", envImpactsValue=10)
    item4 = Item(name="Brain-rot remover device", price=3222, image="brainrotGone.jpg", description='A device which cures mental illnesses or personality disorders. "If you have absolutly ANY mental health problems, this device is a must"- Doctor Bruce Tim Wayne. PLEASE NOTE: This device can only be bought if approved by a professional doctor and requires a medical facility for the implementation.', delivery_time="14-18 working days", environmental_impact="(HIGH). Due to heavy reliance on advanced medical technology and nano tech.", envImpactsValue=8)
    item5 = Item(name="NeuroSpecs", price=99, image="NeuroSpecs.jpg", description="Smart glasses which can solve ANY math or science question you look at (The answer will appear on the bottem left of your vision). Also comes with the latest, most advance AI, Talk-GPT in built into the specs.", delivery_time="4-5 working days", environmental_impact="(MEDIUM). This is because the NeuroSpecs contribute significantly to e-waste and because it uses features such as AR processors and sensors which use a lot of raw earth materials.", envImpactsValue=5)
    item6 = Item(name="Advanced Dumbbell", price=90, image="AdvancedDumbbell.jpg", description="A pair of dumbbells with a weight-changing feature. You may change the weight to any of the following weights: 6kg, 8kg, 10kg, 12kg, 15kg, 18kg, 20kg, 25kg, 30kg. This device is absolutely perfect for those who are into body building. Even gym casuals would find this device useful.", delivery_time="3-4 working days", environmental_impact="(VERY LOW). This product is mostly mechanical and works by using advanced engineering techniques.", envImpactsValue=1)
    item7 = Item(name="The ReCharge Watch", price=8050, image="watch.jpg", description="A smart watch which fully energizes you. With just a simple tap on the screen of the watch, you will stop feeling lazy and will feel exteremely energized. This watch is great for people who need to be very productive or for people who play a lot of sports. You can change the energy levels of the watch in the settings.", delivery_time="6-7 working days", environmental_impact="(HIGH). This watch makes use of an extremely high amount of power due to energy manipulation. It also uses advanced medical technology to manipulate your brian cells into becoming more active.", envImpactsValue=9)
    item8 = Item(name="Temp-Control Hoodie", price=300, image="tempHoodie.jpg", description="A hoodie which varies in thickness and warmth depending on how hot or cold the temperature outside is. You also have the option of changing the temperature by yourself. The Temp-Control Hoodie blends everyday comfort with smart adaptive fabric technology. Using a combination of regular cotton-blend materials and a modest layer of temperature-responsive nano-fibers, the hoodie can automatically adjust its insulation based on environmental conditions without requiring high energy consumption or bulky electronics.", delivery_time="2-3 working days", environmental_impact="(MEDIUM). Although it mostly uses regular fabrics, it also uses nano-fibre.", envImpactsValue=5)

    db.session.add_all([item1, item2, item3, item4, item5, item6, item7,item8])
    db.session.commit()

    print("Database and items created successfully!")
