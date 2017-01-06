import json, uuid
from culqi import Culqi

def main():
    culqi = Culqi("pk_test_vzMuTHoueOMlgUPj","sk_test_UTCQSGcXW8bCyU59")
    token = culqi.createToken("4111111111111111","PEN","123",9,2020,"q352454534","Muro","wmuro@me.com","William")

    print token["id"]

    charge = culqi.createCharge("Avenida Lima 1232","LIMA",1000,"PE","PEN","wmuro@me.com","William",0,"Muro","",
             9899,3333339,"Venta de prueba",token["id"])
    print charge["id"]

    plan = culqi.createPlan("plan-test-"+str(uuid.uuid1()),1000,"PEN","day",2,10,"Plan de Prueba"+str(uuid.uuid1()),50)
    print plan["alias"]

    subscription = culqi.createSubscription("Avenida Lima 123213","LIMA","PE","wmuro@me.com","Muro","William",1234567789,plan["alias"],token["id"])
    print subscription

    refund = culqi.createRefund(500,charge["id"],"give me money back")
    print refund

if __name__ == "__main__":
    main()
