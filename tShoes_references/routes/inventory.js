let express = require('express');
    router = express.Router();
    inventory = require('../controller/inventory.controller');

//----------------
// Methods
//----------------

/**
 * Create inventory
 */
router.post('/designers/:designer/inventory', inventory.createInventory);


module.exports = router;

