//
//  CreateTripVC.swift
//  Trip Planner
//
//  Created by Fernando on 10/17/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

class CreateTripVC: UIViewController {

    @IBOutlet weak var destinationTextField: UITextField!
    @IBOutlet weak var startDateTextField: UITextField!
    @IBOutlet weak var endDateTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    @IBAction func saveTripPressed(_ sender: UIButton) {
        
        let defaults = UserDefaults.standard
        guard let email = defaults.string(forKey: "Email"),
            let password = defaults.string(forKey: "Password")
            else {return}
        
        let basicHeader = BasicAuth.generateBasicAuthHeader(username: email, password: password)
        let trip = Trip(completed: false, destination: self.destinationTextField.text!, start_date: self.startDateTextField.text!, end_date: self.endDateTextField.text!, waypoints: [])
        Networking.instance.fetch(route: Route.trips, method: "POST", headers: ["Authorization": basicHeader, "Content-Type": "application/json"], data: trip) { (data) in
            
            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
            guard let trip = json else {
                return
            }
            
            print(trip)
            
        }
        
    }
    
}
