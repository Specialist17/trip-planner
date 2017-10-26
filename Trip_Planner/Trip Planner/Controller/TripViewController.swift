//
//  TripViewController.swift
//  Trip Planner
//
//  Created by Fernando on 10/16/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

class TripViewController: UIViewController {
    var trip: Trip!
    
    @IBOutlet weak var completedSwitch: UISwitch!
    override func viewDidLoad() {
        super.viewDidLoad()

        completedSwitch.isOn = trip.completed
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func changeCompletedStatus(_ sender: UISwitch) {
        trip.completed = completedSwitch.isOn
        
        Networking.instance.fetch(route: Route.trips, method: "PUT", headers: ["Authorization" : BASIC_AUTH_HEADERS, "Content-Type": "application/json"], data: self.trip) { (data) in
        }
    }
    
    
}
