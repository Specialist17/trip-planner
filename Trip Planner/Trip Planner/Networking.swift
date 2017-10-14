//
//  Networking.swift
//  Trip Planner
//
//  Created by Fernando on 10/14/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import Foundation

enum Route {
    case user
    case trips(tripId: Int)


    // Path
    func path() -> String {
        switch self {
        case .user:
            return "users"
        case .trips:
            return "trips"
        }
    }
    
    // URL Parameters - query
    func urlParameters() -> [String: String] {
        switch self {
        case .user:
            return [:]
        case let .trips(tripId):
            return ["search[postId]": "\(tripId)", "page": "2"]
        }
    }
    
    // Body
    func body() -> Data? {
        switch self {
        case .user:
            return Data()
        default:
            return nil
        }
    }
}


class Networking {
    static let instance = Networking()

    let baseUrlString = "http://127.0.0.1:5000/"
    let session = URLSession.shared

    func fetch(route: Route, headers: [String: String], completion: @escaping (Data) -> Void) {
        let fullUrlString = baseUrlString.appending(route.path())

        let url = URL(string: fullUrlString)!

        var request = URLRequest(url: url)
        request.allHTTPHeaderFields = headers

        session.dataTask(with: request) { (data, response, error) in
            guard let data = data else {
                return
            }

            completion(data)
            }.resume()

    }
}


