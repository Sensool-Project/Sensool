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

    async function createTable(tableName) {
        console.log("Creating Table");
        const params = {
            DatabaseName: "Test3",
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
                    return ("Table " + tableName + " already exists on db Test3. Skipping creation.");
                } else {
                    return ("Error creating table " + tableName + " : " + err);
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
            var succes_insert = await writeRecords("Test3", table, key, JSON.stringify(event[key]), timestamp);
            if (succes_insert.indexOf("The table " + table + " does not exist")!== -1){
                response = response + "Creation de la table " + table +". ";
                var succes_create = await createTable(table);
                response = response + "Creation envoye " + succes_create +". ";
                succes_insert = await writeRecords("Test3", table, key, JSON.stringify(event[key]), timestamp);
            }
            response = response + "Ecriture envoye : key/" + key +" value/" + event[key] + " time/" + timestamp + " table/" + table +". " + succes_insert +". ";
        }
    }
    context.succeed(response);
}
