var express = require('express');
var router = express.Router();
let BasePermission = require('../permissions/permissions').BasePermission;
let auth = new BasePermission();

/* GET home page. */
router.get('/', function(req, res) {
  if(auth.isAuthenticated(req))
  {
    res.render('index', { title: 'Express' });
  }
  else
  {
    res.status(401).json({
      message: "Please send your credentials"
    });
  }
});

module.exports = router;
