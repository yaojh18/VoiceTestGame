var express = require('express');

var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Express' });
});
router.get('/admin', function(req, res, next) {
    res.render('admin', { 'title': 'Admin Page' });
});
router.get('/register', function(req, res, next) {
    res.render('register', { 'title': 'Register Page' });
});
router.get('/login', function(req, res, next) {
    res.render('login', {
        'title': 'Login Page'
    });
});
router.get('/manager', function(req, res, next) {
    res.render('main', {
        'title': 'Manager Page'
    });
});
router.post('/register', function(req, res, next) {
    var user_name = req.body.user;
    var password = req.body.pwd;
    console.log("User name = " + user_name + ", password is " + password);
    res.end("yes");
    res.render('register', { 'title': 'Register Page After' });
});
router.post('/login', function(req, res, next) {
    var user_name = req.body.user;
    var password = req.body.pwd;
    console.log("User name = " + user_name + ", password is " + password);
    res.end("yes");
    res.render('login', { 'title': 'Login Page After ' });
});



module.exports = router;