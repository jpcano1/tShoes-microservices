let InventoryModel = require('../models/models').Inventory;
    fetch = require('node-fetch');

//-------------------
// Methods
//-------------------

let getDesigner = function()
{
    
};

/**
 * Creates a new inventory
 * @param req the request object
 * @param res the response object
 */
exports.postInventory = async (req, res) =>
{
    let data = {
        designer: req.params.designer,
        references: []
    };

    const query = InventoryModel.findOne({designer: data.designer});
    const docs = await query;

    if(docs)
    {
        return res.status(405).json({
            message: "You already have an inventory"
        });
    }

    let model = new InventoryModel(data);
    model.save()
        .then(doc =>
        {
            if(!doc || doc.length === 0)
            {
                return res.status(500).json(doc);
            }
            return res.status(201).json(doc);
        })
        .catch(err =>
        {
            return res.status(500).json(err);
        });
};

/**
 * Gets the inventory of the designer
 * @param req the request object
 * @param res the response object
 */
exports.getInventory = (req, res) =>
{
    if(req.params.designer)
    {
        let designer = req.params.designer;
        InventoryModel.findOne({designer: designer}, (err, doc) =>
        {
            if(err)
            {
                res.status(500).json(err);
            }
            else if(doc)
            {
                res.status(200).json(doc);
            }
            else
            {
                res.status(404).send();
            }
        });
    }
};
