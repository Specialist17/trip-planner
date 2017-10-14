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
        print(basicAuthHeaders)
        Networking.instance.fetch(route: Route.trips(tripId: 1), headers: ["Authorization": basicAuthHeaders]) { (data) in
            
            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
            print(json)
            
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

