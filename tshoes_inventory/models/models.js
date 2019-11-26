let mongoose = require('mongoose');
autoIncrement = require('mongoose-auto-increment');
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
 * Initialize the auto-increment module
 */
autoIncrement.initialize(connection);

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
        type: [Number],
        index: true,
        sparse: true
    }
});

InventorySchema.plugin(autoIncrement.plugin,
    {
        model: 'Inventory',
        field: 'id',
        startAt: 1,
        incrementBy: 1
    });

module.exports = {
    Inventory: connection.model('Inventory', InventorySchema)
};


