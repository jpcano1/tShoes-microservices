let express = require('express');
    router = express.Router();
    references = require('../controller/reference.controller');

//----------------
// Methods
//----------------

/**
 * Create reference
 */
router.post('/designers/:designer/references', references.postReference);

/**
 * Get list of references
 */
router.get('/references', references.getReferences);

/**
 * Get reference detail
 */
router.get('/references/:id', references.getReferenceById);

module.exports = router;

