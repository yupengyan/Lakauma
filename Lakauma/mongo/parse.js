var jsontext = '{"firstname":"Jesper","surname":"Aaberg","phone":["555-0100","555-0120"]}';
var contact = JSON.parse(jsontext);
document.write(contact.surname + ", " + contact.firstname);

var asunnot = [{ "_id" : { "$oid" : "516652e9fffe8ab58e942e16" }, "osoite" : "Kaakkuri 20, 40100", "hinta" : 200 },{ "_id" : { "$oid" : "516655abfffe8ab58e942e17" }, "osoite" : "Kaakkuri 22, 40100", "hinta" : 250 },{ "_id" : { "$oid" : "516655abfffe8ab58e942e18" }, "osoite" : "Kaakkuri 24, 40100", "hinta" : 260 },{ "_id" : { "$oid" : "516655abfffe8ab58e942e19" }, "osoite" : "Kaakkuri 26, 40100", "hinta" : 270 }];
    
for (var i = 0; i < asunnot.length; i++) {
    var asunto = JSON.parse(asunnot[i]);
    document.write(asunto.hinta + ", " + asunto.osoite);
}
    
