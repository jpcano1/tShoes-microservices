var express = require('express');
var router = express.Router();
var inventory = require('../controller/inventory.controller');

/**
 * Creates a new inventory
 */
router.post('/designers/:designer/inventory', inventory.postInventory);

/**
 * Retrieves an inventory
 */
router.get('/designers/:designer/inventory', inventory.getInventory);

/**
 * Updates the inventory
 */
router.put('/designers/:designer/inventory', inventory.updateInventory);

/**
 * Exports the router object
 */
module.exports = router;
