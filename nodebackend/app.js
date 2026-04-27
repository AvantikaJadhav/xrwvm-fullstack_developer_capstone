const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB connection
const MONGO_URL = "mongodb+srv://avantikajadhav81_db_user:avantika@cluster0.plhmsfx.mongodb.net/dealershipsDB?appName=Cluster0";

mongoose.connect(MONGO_URL)
    .then(() => console.log('MongoDB connected!'))
    .catch(err => console.log('MongoDB connection error:', err));

// Review Schema
const reviewSchema = new mongoose.Schema({
    dealerId: Number,
    name: String,
    review: String,
    purchase: Boolean,
    car_make: String,
    car_model: String,
    car_year: Number,
    sentiment: String
});

const Review = mongoose.model('Review', reviewSchema);

// Dealer Schema
const dealerSchema = new mongoose.Schema({
    id: Number,
    city: String,
    state: String,
    st: String,
    address: String,
    zip: String,
    lat: Number,
    long: Number,
    short_name: String,
    full_name: String
});

const Dealer = mongoose.model('Dealer', dealerSchema);

// Add sample data
app.get('/setup', async (req, res) => {
    await Dealer.deleteMany({});
    await Review.deleteMany({});
    
    await Dealer.insertMany([
        { id: 1, city: "Wichita", state: "Kansas", st: "KS", address: "123 Main St", zip: "67201", lat: 37.6872, long: -97.3301, short_name: "Wichita Dealer", full_name: "Cars Dealership Wichita" },
        { id: 2, city: "Topeka", state: "Kansas", st: "KS", address: "456 Oak Ave", zip: "66601", lat: 39.0473, long: -95.6752, short_name: "Topeka Dealer", full_name: "Cars Dealership Topeka" },
        { id: 3, city: "Chicago", state: "Illinois", st: "IL", address: "789 Lake St", zip: "60601", lat: 41.8781, long: -87.6298, short_name: "Chicago Dealer", full_name: "Cars Dealership Chicago" }
    ]);

    await Review.insertMany([
        { dealerId: 1, name: "John Doe", review: "Great service!", purchase: true, car_make: "Toyota", car_model: "Camry", car_year: 2022, sentiment: "positive" },
        { dealerId: 1, name: "Jane Smith", review: "Very helpful staff.", purchase: true, car_make: "Honda", car_model: "Civic", car_year: 2021, sentiment: "positive" },
        { dealerId: 2, name: "Bob Johnson", review: "Good experience overall.", purchase: false, car_make: "Ford", car_model: "Mustang", car_year: 2023, sentiment: "positive" }
    ]);

    res.json({ message: "Sample data added successfully!" });
});

// Get all dealers
app.get('/fetchDealers', async (req, res) => {
    const dealers = await Dealer.find({});
    res.json({ dealers });
});

// Get dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
    const dealer = await Dealer.findOne({ id: parseInt(req.params.id) });
    res.json({ dealer });
});

// Get dealers by state
app.get('/fetchDealers/:state', async (req, res) => {
    const dealers = await Dealer.find({ state: req.params.state });
    res.json({ dealers });
});

// Get reviews by dealer ID
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    const reviews = await Review.find({ dealerId: parseInt(req.params.id) });
    res.json({ reviews });
});

// Insert a review
app.post('/insertReview', async (req, res) => {
    try {
        const { name, dealership, review, purchase, car_make, car_model, car_year } = req.body;
        const newReview = new Review({
            dealerId: dealership,
            name,
            review,
            purchase,
            car_make,
            car_model,
            car_year,
            sentiment: 'positive'
        });
        await newReview.save();
        res.json({ message: 'Review inserted successfully!', review: newReview });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Car Make Schema
const carMakeSchema = new mongoose.Schema({
    id: Number,
    name: String,
    models: [{ id: Number, name: String }]
});

const CarMake = mongoose.model('CarMake', carMakeSchema);

// Setup car makes
app.get('/setupcars', async (req, res) => {
    await CarMake.deleteMany({});
    await CarMake.insertMany([
        { id: 1, name: "Toyota", models: [{ id: 1, name: "Camry" }, { id: 2, name: "Corolla" }, { id: 3, name: "RAV4" }] },
        { id: 2, name: "Honda", models: [{ id: 1, name: "Civic" }, { id: 2, name: "Accord" }, { id: 3, name: "CR-V" }] },
        { id: 3, name: "Ford", models: [{ id: 1, name: "Mustang" }, { id: 2, name: "F-150" }, { id: 3, name: "Explorer" }] },
        { id: 4, name: "Chevrolet", models: [{ id: 1, name: "Silverado" }, { id: 2, name: "Malibu" }, { id: 3, name: "Equinox" }] }
    ]);
    res.json({ message: "Car makes added successfully!" });
});

// Get all car makes
app.get('/fetchCars', async (req, res) => {
    const cars = await CarMake.find({});
    res.json({ cars });
});

app.listen(3000, () => {
    console.log('Node server running on port 3000');
});