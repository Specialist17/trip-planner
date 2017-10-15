//
//  ViewController.swift
//  Trip Planner
//
//  Created by Fernando on 10/13/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        let basicAuthHeaders = BasicAuth.generateBasicAuthHeader(username: "fernando2@mail.com", password: "password")
        
        Networking.instance.fetch(route: Route.trips, headers: ["Authorization": basicAuthHeaders]) { (data) in
            
//            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
//            if let trips = json {
//                print(trips)
//                print(type(of: trips))
//            }
            
            let trips = try? JSONDecoder().decode(Trip.self, from: data)
            guard let trip_list = trips?.trips else {return}
            print(trip_list)
            
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

