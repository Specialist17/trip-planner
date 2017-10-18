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
        print(defaults.string(forKey: "Email"))
        if let _ = defaults.string(forKey: "Email"){
            print("hello")
            self.performSegue(withIdentifier: "HomeSegue", sender: self)
        }
       
        // Do any additional setup after loading the view.
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
        
        defaults.set(username, forKey: "Email")
        defaults.set(password, forKey: "Password")
        
        let basicHeader = BasicAuth.generateBasicAuthHeader(username: username, password: password)
        Networking.instance.fetch(route: Route.user, method: "GET", headers: ["Authorization": basicHeader], data: nil) { (data) in
            
            let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
            guard let user = json else {
                return
            }
            
            print(user)
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
        defaults.set(email, forKey: "Email")
        defaults.set(password, forKey: "Password")
        
        let user = User(username: "El usuario", email: email, password: password)
        
        Networking.instance.fetch(route: Route.user, method: "POST", headers: ["Content-Type": "application/json"], data: user) { (data) in
            
            
            DispatchQueue.main.async {
                self.performSegue(withIdentifier: "HomeSegue", sender: sender)
            }
        }
        
        
    }
    
}
