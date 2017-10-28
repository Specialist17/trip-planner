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
    let defaults = UserDefaults.standard
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        let loggedIn = UserDefaults.standard.bool(forKey: "isLoggedIn")
        if loggedIn {
            self.performSegue(withIdentifier: "HomeSegue", sender: self)
        }
        self.view.addGestureRecognizer(UITapGestureRecognizer(target: self.view, action: #selector(UIView.endEditing(_:))))
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func performLogin(_ sender: UIButton) {
        
        guard let username = self.emailTextField.text,
         let password = self.passwordTextField.text else {
            return
        }
        
        let basicHeader = BasicAuth.generateBasicAuthHeader(username: username, password: password)
        defaults.set(basicHeader, forKey: "basicAuth")
        defaults.set(true, forKey: "isLoggedIn")
        Networking.instance.fetch(route: Route.user, method: "GET", headers: ["Authorization": basicHeader], data: nil) { (data) in
            print("hola")
            DispatchQueue.main.async {
                self.performSegue(withIdentifier: "HomeSegue", sender: sender)
            }
        }
    }
    
    
    @IBAction func performSignup(_ sender: UIButton) {
        
        guard let email = self.emailTextField.text,
            let password = self.passwordTextField.text else {
                return
        }
        
        let defaults = UserDefaults.standard
        
        let basicHeader = BasicAuth.generateBasicAuthHeader(username: email, password: password)
        let user = User(username: "El usuario", email: email, password: password)
        defaults.set(basicHeader, forKey: "basicAuth")
        defaults.set(true, forKey: "isLoggedIn")
        
        Networking.instance.fetch(route: Route.user, method: "POST", headers: ["Content-Type": "application/json"], data: user) { (data) in
            
            
            DispatchQueue.main.async {
                self.performSegue(withIdentifier: "HomeSegue", sender: sender)
            }
        }
    }
}
