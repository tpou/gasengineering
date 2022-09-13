var express             = require("express"),
    mongoose            = require("mongoose"),
    mongoclient         = require("mongodb").MongoClient,
    //Fluiddymo           = require("./models/fluiddymo"),
    //Movies              = require("./models/movies"),
    bodyParser          = require("body-parser");

const url ="mongodb+srv://oilgas:oilgas-password@gasproperty-engxm.mongodb.net/test?retryWrites=true&w=majority";
const db_name = "gasproperty"

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine","ejs");

var db, collectionOne, collectionTwo, resultsOne, resultsTwo, fluidprops, fluidpropsactive;

app.listen(3000, () => {
    mongoclient.connect(url, {useNewUrlParser: true}, (err, client)=>{
        if(err) {
            console.log(err)
        } else {
            db = client.db(db_name);
            collectionOne = db.collection("fluid_thermo");
            collectionTwo = db.collection("fluid_thermo_active");
            console.log("Connect to...");
        }
    })
})
    

app.get("/", function(req, res){
    res.render("home");
});


app.get("/bg", function(req, res){
    
    collectionOne.find().toArray((err, resultsOne) => {
        if(err){
            console.log(err)
        } else {
            res.render("bg/index", {fluidprops: resultsOne});
            
        }
    })
    collectionTwo.find().toArray((err, resultsTwo)=>{
        if(err){
            console.log(err)
        } else {
            console.log(resultsTwo)
            //res.render("bg/index",{fluidpropsactive: resultsTwo});
           
        }
    })
    // res.render("bg/index", {
    //     fluidprops: resultsOne,
    //     fluidpropsactive: resultsTwo
    // })
    
});

//add new compound to current db
app.post("/bg", function(req, res){
    console.log("test")
   
   res.redirect("/bg") 
});

app.get("/bg/new", function(req, res){
    res.render("bg/new");
});

app.listen(process.env.PORT,process.IP, function(){
    console.log("Server started!!!");
})