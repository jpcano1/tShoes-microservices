var express = require('express');
var router = express.Router();
var inventory = require('../controller/inventory.controller');

router.post('/designers/:designer/inventory', inventory.postInventory);
router.get('/designers/:designer/inventory', inventory.getInventory);
module.exports = router;
