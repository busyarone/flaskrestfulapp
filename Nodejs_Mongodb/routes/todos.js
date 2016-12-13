var express = require('express');
var router = express.Router();

var mongoose = require('mongoose');
var Todo = require('../models/Todo.js');

/* GET users listing. */
/*router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});*/


/* GET /todos listing. */
router.get('/', function(req, res, next) {
  Todo.find(function (err, todos) {
    if (err) return next(err);
    res.json(todos);
  });
});


/* POST /todos */
router.post('/', function(req, res, next) {
  //console.log(req.body);
  //console.log(req.body.updated_at);
  var data = {}
  data['updated_at'] = new Date(req.body.updated_at);
  data['name']= req.body.name;;
  data['completed']=req.body.completed;
  data['notes']=req.body.notes;
  Todo.create(data, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

/* GET by Id*/
router.get('/:id', function(req, res, next) {
  Todo.findById(req.params.id, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

/*Update Id*/
router.put('/:id', function(req, res, next) {
  Todo.findByIdAndUpdate(req.params.id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

/* DELETE /todos/:id */
router.delete('/:id', function(req, res, next) {
  Todo.findByIdAndRemove(req.params.id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

/* Search*/
router.get('/search', function(req, res, next) {
  console.log('Search operation');
  //Todo.findById(req.params.id, function (err, post) {
  	// if (err) return next(err);
   // res.json(post);
  //});
});



module.exports = router;
