//
//  Trip.swift
//  Trip Planner
//
//  Created by Fernando on 10/14/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

struct Waypoint: Codable {
    let destination: String
    let location: [String: Double]
}

struct Trip: Codable {
    
    var completed: Bool
    var destination: String
    var start_date: String
    var end_date: String
    var waypoints: [Waypoint]

}

