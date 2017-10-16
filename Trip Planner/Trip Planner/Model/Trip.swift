//
//  Trip.swift
//  Trip Planner
//
//  Created by Fernando on 10/14/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

struct Trip: Codable {
    
//    var id: String!
    var completed: Bool!
    var destination: String!
    var start_date: String!
    var end_date: String!
    var trips = [Trip]()
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
        case trips
//        case id = "_id"
        enum TripKeys: String, CodingKey{
            case completed
            case destination
            case start_date
            case end_date
        }
        
//        case waypoints
    }
    
    
    init(from decoder: Decoder) throws {
        // Go into main container
        var searchContainer = try decoder.container(keyedBy: TripsKeys.self)
        
        // Get the array of unkeyed listings container
        var tripsContainer = try searchContainer.nestedUnkeyedContainer(forKey: .trips)
        print(tripsContainer.count)
        
        // loop through every listing element
        while !tripsContainer.isAtEnd {
            
            // access the current result container - {listing: value, pricing_quote: value}
            let container = try tripsContainer.nestedContainer(keyedBy: TripsKeys.TripKeys.self)
            
            
            // get specified values for the listing
            let completed = try container.decode(Bool.self, forKey: .completed)
            let destination = try container.decode(String.self, forKey: .destination)
            
            let startDate = try container.decode(String.self, forKey: .end_date)
            let endDate = try container.decode(String.self, forKey: .start_date)
            
            // initialize a listing object
            let trip = Trip(completed: completed, destination: destination, start_date: startDate, end_date: endDate)
            
            // add the listing object to the structs listings arrays
            self.trips.append(trip)
        }
    }
}

extension Trip {
    func encode(to encoder: Encoder) throws {
        
    }
}
