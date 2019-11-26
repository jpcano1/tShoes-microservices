let ReferenceModel = require('../models/models').Reference;

//-------------------
// Methods
//-------------------

/**
 *
 * @param req
 * @param res
 * @returns {*|Promise<any>}
 */
exports.postReference = async function(req, res)
{};

/**
 *
 * @param req
 * @param res
 */
exports.getReferences = (req, res) =>
{
    if(req.query.id)
    {
        ReferenceModel.findOne({
            id: req.query.id
        })
            .then(doc =>
            {
                res.status(200).json(doc);
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
    else
    {
        ReferenceModel.find({})
            .then(doc =>
            {
                res.status(200).json(doc);
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
exports.getReferenceById = function(req, res)
{
    if(req.params.id)
    {
        let id = req.params.id;
        ReferenceModel.findOne({
            id: id
        })
            .then(doc =>
            {
                if(doc)
                {
                    res.json(doc);
                }
                else
                {
                    res.status(404).send();
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
exports.updateReference = function(req, res)
{
    if(req.body)
    {
        ReferenceModel.findOneAndUpdate(
            {
                id: req.params.id
            },
            req.body,
            {
                new: true
            })
            .then(doc =>
            {
                res.status(201).json(doc);
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
exports.deleteReference = function(req, res)
{
    if(req.params.id)
    {
        let id = req.params.id;
        ReferenceModel.findOneAndRemove({
            id: id
        })
            .then(doc =>
            {
                res.status(204).send();
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
};
