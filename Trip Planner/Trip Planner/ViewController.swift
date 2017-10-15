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
        let basicAuthHeaders = BasicAuth.generateBasicAuthHeader(username: "fernando@mail.com", password: "password")
        
        Networking.instance.fetch(route: Route.trips(tripId: 1), headers: ["Authorization": basicAuthHeaders]) { (data) in
            
            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
            
            guard let trips = json as Array else {
                return
            }
            
            for item in trips {
                print(item)
            }
            
//            let trips = try? JSONDecoder().decode(Trip.self, from: data)
//
//            print(trips)
            
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

