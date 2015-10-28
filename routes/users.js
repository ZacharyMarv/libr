var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});
router.get('/test2', function(req, res, next) {
  res.render('web2', { title: 'Express'});
});
router.get('/test1', function(req, res, next) {
  res.render('test', { title: 'Express'});
});
router.get('/test3', function(req, res, next) {
  res.render('web3', { title: 'Express'});
});
router.get('/test4', function(req, res, next) {
  res.render('web4', { title: 'Express'});
});
router.get('/test5', function(req, res, next) {
  res.render('web5', { title: 'Express'});
});
module.exports = router;
