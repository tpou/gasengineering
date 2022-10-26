var express             = require("express"),
    mongoose            = require("mongoose"),
    mongoclient         = require("mongodb").MongoClient,
    //Fluiddymo           = require("./models/fluiddymo"),
    //Movies              = require("./models/movies"),
    bodyParser          = require("body-parser");

const url ="mongodb+srv://oilgas:oilgas-password@gasproperty-engxm.mongodb.net/?retryWrites=true&w=majority";
const db_name = "gasproperty"

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine","ejs");

// root static files
app.use(express.static("public"))
// Build markdown

 /// Built-in module to access and interact with the file system
const fs = require("fs");
 /// To parse front matter from Markdown files
const matter = require("gray-matter");

const getPosts = () => {
    // Get the posts from directory
    const posts = fs.readdirSync(__dirname + "/views/posts").filter((post) => post.endsWith(".md"))
    // Set the post content as an empty array
    const postContent = []
    // Inject into the post content array the front matter
    posts.forEach((post) => {
        postContent.push(matter.read(__dirname +"/views/posts/" + post))
    })
    /**
     * 1 - Return a list of posts as a two dimensional array containing for each one:
     * . the post filename with it's extension (e.g : postFilename.md)
     * . the post content as an object {content:"Markdown content as a string", data:{front matter}, excerpt:""}
     * 2- Return each array as an object and create a Date instance from it's date front matter
     * 3- Sort posts by publication's date in descending order (newest to odest)
     */
    const postsList = posts
        .map(function (post,i) {
            return [post, postContent[i]]
        })
        .map((obj) => {
            return {...obj, date: new Date(obj[1].data.date)}
        })
        .sort((objA, objB) => Number(objB.date) - Number(objA.date))
    return postsList
}

 /// Render the list of posts on the main route
app.get("/blog", (req, res) => {
    res.render("postsList", {
        posts: getPosts(),
    })
})

 /// Using a route parameter to render each post on a route matching it's filename
app.get("/posts/:post", (req, res) => {
    const postTitle = req.params.post // Get the Markdown filename

    // Read the Markdown file and parse it's front matter
    const post = matter.read(__dirname + "/views/posts/" +postTitle +".md")
    // Convert the Markdown file content to HTML with markdown-it
    const md = require("markdown-it")({html: true}) // Allows HTML tags inside the Markdown file
    const content = post.content // Read the Markdown file content
    const html = md.render(content) // Convert the Markdown file content to HTML

    // Render the postsTemplate for each post and pass it's front matter as a data object into postsTemplate
    res.render("postsTemplate", {
        title: post.data.title,
        date: post.data.date,
        postContent: html,
    })
})

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
    // res.render("home");
    collectionOne.find().toArray((err, resultsOne) => {
        if(err){
            console.log(err)
        } else {
            res.render("index", {fluidprops: resultsOne});

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
});


app.get("/bg", function(req, res){
    
    collectionOne.find().toArray((err, resultsOne) => {
        if(err){
            console.log(err)
        } else {
            res.render("bg/bg", {fluidprops: resultsOne});
            
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