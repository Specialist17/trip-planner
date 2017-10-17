//
//  LoginVC.swift
//  Trip Planner
//
//  Created by Fernando on 10/16/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

class LoginVC: UIViewController {

    @IBOutlet weak var emailTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
       
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func performLogin(_ sender: UIButton) {
        print("hello")
        let basicAuthHeaders = BasicAuth.generateBasicAuthHeader(username: "fernando2@mail.com", password: "password")
        
        Networking.instance.fetch(route: Route.user, method: "GET", headers: ["Authorization": basicAuthHeaders], data: nil) { (data) in
            
            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
            guard let user = json else {
                return
            }
            
            print(user)
            
        }
    }
    
    
    @IBAction func performSignup(_ sender: UIButton) {
        Networking.instance.fetch(route: Route.user, method: "POST", headers: [:], data: nil) { (data) in
            
            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
            guard let user = json else {
                return
            }
            
            print(user)
            
        }
    }
    
}
