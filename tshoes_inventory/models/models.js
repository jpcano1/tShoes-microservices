let mongoose = require('mongoose');
Schema = mongoose.Schema;

const username = process.env.MONGO_USER;
const password = process.env.MONGO_PASSWORD;
const host = process.env.MONGO_HOST;
const uri = `mongodb+srv://${username}:${password}@${host}/test?retryWrites=true&w=majority`;

/**
 * Connection to mongo atlas db
 */
let connection = mongoose.createConnection(uri, {
    useNewUrlParser: true
});

/**
 * Create the schema for the inventory
 * @type {Mongoose.Schema}
 */
let InventorySchema = new Schema({
    designer: {
        type: Number,
        required: true
    },
    references: {
        type: [Object],
        index: true,
        sparse: true
    }
});

module.exports = {
    Inventory: connection.model('Inventory', InventorySchema)
};


