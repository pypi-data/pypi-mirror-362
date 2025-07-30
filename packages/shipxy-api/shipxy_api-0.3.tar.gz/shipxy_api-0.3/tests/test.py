from shipxy import Shipxy

from key import key
# key = "请从 API控制台 申请";

if __name__ == '__main__':
    # response = Shipxy.SearchShip(key, "coco")
    # response = Shipxy.GetSingleShip(key, 413961925)
    # response = Shipxy.GetManyShip(key, "413961925,477232800,477172700")
    # response = Shipxy.GetFleetShip(key, "f777007b-fb88-4c4c-b4eb-db33e84e99ee")
    # response = Shipxy.GetSurRoundingShip(key, 413961925)
    # response = Shipxy.GetAreaShip(key, "121.289063,35.424868-122.783203,35.281501-122.167969,33.979809")
    # response = Shipxy.GetShipRegistry(key, 413961925)
    # response = Shipxy.SearchShipParticular(key, 477172700)

    # response = Shipxy.SearchPort(key, "qingdao")
    # response = Shipxy.GetBerthShips(key, "CNSHG", 99)
    # response = Shipxy.GetAnchorShips(key, "CNSHG", 52)
    # response = Shipxy.GetETAShips(key, "CNSHG", 1746612218, 1747044218)

    # response = Shipxy.GetShipTrack(key, 477172700, 1746612218, 1747044218)
    # response = Shipxy.SearchshipApproach(key, 477172700, 1746612218, 1747044218)

    # response = Shipxy.GetPortofCallByShip(key, 477172700, 1751007589, 1751440378)
    # response = Shipxy.GetPortofCallByShipPort(key, 477172700, 'CNSHG', 1751007589, 1751440378)
    # response = Shipxy.GetShipStatus(key, 477172700)
    # response = Shipxy.GetPortofCallByPort(key, 'CNSHG', 1751407589, 1751411189)

    # response = Shipxy.PlanRouteByPoint(key, '113.571144,22.844316', "121.58414,31.37979")
    # response = Shipxy.PlanRouteByPort(key, 'CNGZG', "CNSHG")
    # response = Shipxy.GetSingleETAPrecise(key,  477172700,  "CNSHG", 20)

    # response = Shipxy.GetWeatherByPoint(key, 123.58414, 27.37979)
    # response = Shipxy.GetWeather(key, 1)
    # response = Shipxy.GetAllTyphoon(key)
    # response = Shipxy.GetSingleTyphoon(key, 2477927)
    # response = Shipxy.GetTides(key)
    # response = Shipxy.GetTideData(key, "8000005", '2025-03-01', '2025-03-05')

    # response = Shipxy.GetNavWarning(key, '2024-07-21 20:00', '2024-09-21 20:00', 2)

    # response = Shipxy.AddFleet(key, "测试船队5", "477985705,412751695", 1)
    # response = Shipxy.UpdateFleet(key, '0372ec4c-eead-49ce-b005-6ffa731cc1df', "测试船队", "477985700", 1)
    # response = Shipxy.GetFleet(key, '0372ec4c-eead-49ce-b005-6ffa731cc1df')
    # response = Shipxy.DeleteFleet(key, '4956ee93-e8dc-4aa0-aee7-483cf80fc950')
    # response = Shipxy.AddFleetShip(key, '0372ec4c-eead-49ce-b005-6ffa731cc1df',  "477985700,412751690")
    # response = Shipxy.UpdateFleetShip(key, '0372ec4c-eead-49ce-b005-6ffa731cc1df', "477985700")
    # response = Shipxy.DeleteFleetShip(key, '0372ec4c-eead-49ce-b005-6ffa731cc1df', "477985700")

    # response = Shipxy.AddArea(key, "119.846180,32.345143-119.814280,32.311867-119.4661,32.291067-119.375887,32.213847",
    #                           "浙江沿海区域1", "http://192.186.1.1:8000/Shipxy/testdemo",
    #                           3, "59","1,2,3", "0372ec4c-eead-49ce-b005-6ffa731cc1df")

    # response = Shipxy.UpdateArea(key, "075451e6-0ffa-44d4-94d2-adbf17d862a5",
    #                              "119.846180,32.345143-119.814280,32.311867-119.4661,32.291067-119.375887,32.213847",
    #                              "浙江沿海区域", "http://192.186.1.1:8000/Shipxy/testdemo",
    #                              3, 59, "1,2,3", "c02def78-a57d-4311-bee3-1c89a018cddf")
    # response = Shipxy.GetArea(key, '075451e6-0ffa-44d4-94d2-adbf17d862a5')
    response = Shipxy.DeleteArea(key, 'c7b5436f-5e73-4087-aeba-93add7f39f17')

    print(response)
    # print("test")