var express = require('express');
var router = express.Router();
var inventory = require('../controller/inventory.controller');

router.post('/designers/:designer/inventory', inventory.postInventory);

module.exports = router;
