let InventoryModel = require('../models/models').Inventory;

//-------------------
// Methods
//-------------------

/**
 *
 * @param req
 * @param res
 */
exports.getInventory = (req, res) =>
{
    if(req.params)
    {
        let designer = req.params.designer;
        InventoryModel.findOne({
            designer: designer
        })
            .then(doc =>
            {
                if(doc)
                {
                    return res.json(doc);
                }
                else
                {
                    res.status(404).json({
                        message: "You don't have an inventory yet"
                    });
                }
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
};

/**
 *
 * @param req
 * @param res
 */
exports.createInventory = function(req, res)
{
    if(req.params)
    {
        let designer = req.params.designer;
        let model = new InventoryModel({
            designer: designer
        });
        model.save()
            .then(doc =>
            {
                if(!doc || doc.length === 0)
                {
                    return res.status(500).send(doc);
                }
                res.status(201).send(doc);
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
};
