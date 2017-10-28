//
//  CreateTripVC.swift
//  Trip Planner
//
//  Created by Fernando on 10/17/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit
import KeychainSwift

class CreateTripVC: UIViewController {

    @IBOutlet weak var destinationTextField: UITextField!
    @IBOutlet weak var startDateTextField: UITextField!
    @IBOutlet weak var endDateTextField: UITextField!
    let keychain = KeychainSwift()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.addGestureRecognizer(UITapGestureRecognizer(target: self.view, action: #selector(UIView.endEditing(_:))))
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func saveTripPressed(_ sender: UIButton) {

        guard let basicHeader = keychain.get("basicAuth")else {return}
        let trip = Trip(completed: false, destination: self.destinationTextField.text!, start_date: self.startDateTextField.text!, end_date: self.endDateTextField.text!, waypoints: [])
        Networking.instance.fetch(route: Route.trips, method: "POST", headers: ["Authorization": basicHeader, "Content-Type": "application/json"], data: trip) { (data) in
            
            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
            guard let trip = json else {
                return
            }
            
            print(trip)
            
        }
        self.dismiss(animated: true, completion: nil)
    }
    
}
