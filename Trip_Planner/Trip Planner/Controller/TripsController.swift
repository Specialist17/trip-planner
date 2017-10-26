//
//  ViewController.swift
//  Trip Planner
//
//  Created by Fernando on 10/13/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

class TripsController: UIViewController {

    @IBOutlet weak var tableView: UITableView!
    var refresher: UIRefreshControl!
    var trips = [Trip]() {
        didSet{
            tableView.reloadData()
        }
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        
        refresher = UIRefreshControl()
        tableView.addSubview(refresher)
        refresher.attributedTitle = NSAttributedString(string: "Pull to refresh")
        refresher.tintColor = UIColor(red: 1.00, green: 130/255, blue: 45/255, alpha: 0.8)
        refresher.addTarget(self, action: #selector(getTrips), for: .valueChanged)
        getTrips()
    }
    
    @objc func getTrips() {
        let defaults = UserDefaults.standard
        guard let email = defaults.string(forKey: "Email"),
            let password = defaults.string(forKey: "Password")
            else {return}
        
        let basicHeader = defaults.string(forKey: "basicAuth")
        
        Networking.instance.fetch(route: Route.trips, method: "GET", headers: ["Authorization": basicHeader!], data: nil) { (data) in
            
            let trips = try? JSONDecoder().decode([Trip].self, from: data)
            guard let trip_list = trips else {return}
            DispatchQueue.main.async {
                self.trips = trip_list
                self.refresher.endRefreshing()
            }
            
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}

extension TripsController: UITableViewDelegate, UITableViewDataSource{
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return trips.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "TripCell", for: indexPath) as! TripCell
        
        let trip = trips[indexPath.row]
        cell.configureCell(trip: trip)
        
        let cellAudioButton = UIButton(type: .custom)
        
        cellAudioButton.frame = CGRect(x: 0, y: 0, width: 30, height: 30)
        cellAudioButton.addTarget(self, action: #selector(self.accessoryButtonTapped(sender:)), for: .touchUpInside)
        if trip.completed {
            
            cellAudioButton.setImage(UIImage(named: "checked.png"), for: .normal)
        } else {
            cellAudioButton.setImage(UIImage(named: "unchecked.png"), for: .normal)
        }
        
        cellAudioButton.contentMode = .scaleAspectFit
        cellAudioButton.tag = indexPath.row
        
        cell.accessoryView = cellAudioButton as UIView
        
        return cell
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    @objc func accessoryButtonTapped(sender : UIButton){
    
        
        var trip = trips[sender.tag]
        
        if trip.completed {
            trip.completed = false
//            completedTasks.remove(at: (completedTasks.count - 1) - sender.tag)
            sender.setImage(UIImage(named: "unchecked.png"), for: .normal)
        } else {
            sender.setImage(UIImage(named: "checked.png"), for: .normal)
            trip.completed = true
//            completedTasks.append(task)
        }
        
        
        
        let defaults = UserDefaults.standard
        guard let email = defaults.string(forKey: "Email"),
            let password = defaults.string(forKey: "Password")
            else {return}
        
        let basicHeader = BasicAuth.generateBasicAuthHeader(username: email, password: password)
        Networking.instance.fetch(route: Route.trips, method: "PUT", headers: ["Authorization" : basicHeader, "Content-Type": "application/json"], data: trip) { (data) in
            DispatchQueue.main.async {
                let buttonPosition = sender.convert(CGPoint.zero, to: self.tableView)
                let indexPath = self.tableView.indexPathForRow(at: buttonPosition)
                if let path = indexPath {
                    self.tableView.reloadRows(at: [path], with: .bottom)
                }
            }
        }
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let trip = trips[indexPath.row]
        performSegue(withIdentifier: "ViewTrip", sender: trip)
    }
}

extension TripsController {
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "ViewTrip" {
            if let destinationVC = segue.destination as? TripViewController{
                if let trip = sender as? Trip {
                    destinationVC.trip = trip
                }
            }
        }
    }
}
