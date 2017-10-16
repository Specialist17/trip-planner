//
//  User.swift
//  Trip Planner
//
//  Created by Fernando on 10/14/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

struct User: Decodable {
    var username: String!
    var email: String!
    var password: String!
    
    init(username: String, email: String, password: String) {
        self.username = username
        self.email = email
        self.password = password
    }
}
