//
//  User.swift
//  Trip Planner
//
//  Created by Fernando on 10/14/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

struct User: Decodable {
    var id: Int!
    var username: String!
    var email: String!
    var password: String!
    var trips: [Trip]
    
    
    init(id: Int, username: String, email: String, password: String, trips: [Trip]) {
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.trips = trips
    }
}
