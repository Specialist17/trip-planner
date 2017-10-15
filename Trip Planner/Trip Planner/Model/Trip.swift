//
//  Trip.swift
//  Trip Planner
//
//  Created by Fernando on 10/14/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

struct Trip: Decodable {
    
//    var id: String!
    var completed: Bool!
    var destination: String!
    var start_date: String!
    var end_date: String!
//    var waypoints: [Dictionary<String, Any>]
//    waypoints: [Dictionary<String, Any>]
//    id: String,
    init(completed: Bool, destination: String, start_date: String, end_date: String) {
//        self.id = id
        self.completed = completed
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
//        self.waypoints = waypoints
    }
}

extension Trip {
    
    enum TripsKeys: String, CodingKey {
//        case id = "_id"
        case completed
        case destination
        case start_date
        case end_date
//        case waypoints
    }
    
    
    init(from decoder: Decoder) throws {
        
        let tripsContainer = try decoder.container(keyedBy: TripsKeys.self)
//        let id = try tripsContainer.decode(String.self, forKey: .id)
        let completed = try tripsContainer.decode(Bool.self, forKey: .completed)
        let destination = try tripsContainer.decode(String.self, forKey: .destination)
        let startDate = try tripsContainer.decode(String.self, forKey: .start_date)
        let endDate = try tripsContainer.decode(String.self, forKey: .end_date)
//        let waypoints = try tripsContainer.decode([Dictionary<String, Any>].self, forKey: .waypoints)
        
        self.init(completed: completed, destination: destination, start_date: startDate, end_date: endDate)
    }
}
