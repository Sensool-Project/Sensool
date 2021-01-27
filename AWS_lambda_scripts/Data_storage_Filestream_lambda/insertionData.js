const AWS = require("aws-sdk");
var https = require("https");

exports.handler = async function(event, context, callback) {
    AWS.config.update({ region: "us-east-2" });

    var agent = new https.Agent({
        maxSockets: 5000
    });
    writeClient = new AWS.TimestreamWrite({
        maxRetries: 10,
        httpOptions: {
            timeout: 20000,
            agent: agent
        }
    });

    queryClient = new AWS.TimestreamQuery();

    async function createTable(database, tableName) {
        console.log("Creation de table");
        const params = {
            DatabaseName: database,
            TableName: tableName,
            RetentionProperties: {
                MemoryStoreRetentionPeriodInHours: 24,
                MagneticStoreRetentionPeriodInDays: 7
            }
        };
    
        const promise = writeClient.createTable(params).promise();
    
        var retour = await promise.then(
            (data) => {
                return ("Table : " + tableName + " cree.");
            },
            (err) => {
                if (err.code === 'ConflictException') {
                    return ("La table " + tableName + " existe deja sur " + database + ". Creation ignore.");
                } else {
                    return ("Erreur a la creation de la table " + tableName + " : " + err);
                }
            }
        );
        return retour;
    }

    async function writeRecords(database, table, nom, valeur, time) {
        console.log("Writing records");

        const dimensions = [
            {'Name': 'region', 'Value': 'us-east-2'},
            {'Name': 'az', 'Value': 'az1'},
            {'Name': 'hostname', 'Value': 'host1'}
        ];
    
        const valeurTest = {
            'Dimensions': dimensions,
            'MeasureName': nom,
            'MeasureValue': valeur,
            'MeasureValueType': 'DOUBLE',
            'Time': time
        };
    
        const records = [valeurTest];
    
        const params = {
            DatabaseName: database,
            TableName: table,
            Records: records
        };
    
        const request = writeClient.writeRecords(params);
    
        var retour = await request.promise().then(
            (data) => {
                return ("Write records successful");
            },
            (err) => {
                if (err.code === 'RejectedRecordsException') {
                    var retour = err + err.response;
                    return("Error writing records:" + retour);
                }
                return("Error writing records:" + err);
            }
        );
        return retour;
    }

    var response = "";
    var timestamp = "";
    var table = "";

    if(event.time){
        var time = new Date(event.time*1000);
        timestamp = Date.parse(time).toString();
        response = "Date : " + timestamp + " : " + time + ". ";
    }
    else {
        response = "Le temps n'a pas été renseigné. ";
        context.succeed(response);
    }
    if(event.table){
        table = event.table;
        response = response + "Table : " + table + ". ";
    }
    else {
        response = "La table n'a pas été renseignée. ";
        context.succeed(response);
    }
    for (const key in event) {
        if(key != "time" && key != "table"){
            response = response + "Valeur trouve. "
            var succes_insert = await writeRecords("Sensool", table, key, JSON.stringify(event[key]), timestamp);
            if (succes_insert.indexOf("The table " + table + " does not exist")!== -1){
                response = response + "Creation de la table " + table +". ";
                var succes_create = await createTable("Sensool", table);
                response = response + "Creation envoye " + succes_create +". ";
                succes_insert = await writeRecords("Sensool", table, key, JSON.stringify(event[key]), timestamp);
            }
            response = response + "Ecriture envoye : key/" + key +" value/" + event[key] + " time/" + timestamp + " table/" + table +". " + succes_insert +". ";
        }
    }

    const ggSdk = require('aws-greengrass-core-sdk');

    const iotClient = new ggSdk.IotData();
    const os = require('os');
    const util = require('util');

    function publishCallback(err, data) {
        console.log(err);
        console.log(data);
    }

    const myPlatform = util.format('%s-%s', os.platform(), os.release());
    const pubOpt = {
        topic: 'servo/trigger',
        payload: JSON.stringify({ message: util.format('Hello world! Sent from Greengrass Core running on platform: %s using NodeJS', myPlatform) }),
        queueFullPolicy: 'AllOrError',
    };

    function greengrassHelloWorldRun() {
        iotClient.publish(pubOpt, publishCallback);
        response = response + "testgreengrass";
    }

    // Schedule the job to run every 5 seconds
    setInterval(greengrassHelloWorldRun, 5000);

    // This is a handler which does nothing for this example
    exports.handler = function handler(event, context) {
        console.log(event);
        console.log(context);
    };
    context.succeed(response);
}