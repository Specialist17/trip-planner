//
//  TripCell.swift
//  Trip Planner
//
//  Created by Fernando on 10/16/17.
//  Copyright © 2017 Specialist. All rights reserved.
//

import UIKit

class TripCell: UITableViewCell {

    @IBOutlet weak var tripDestinationLabel: UILabel!
    @IBOutlet weak var completedButton: UIButton!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // Configure the view for the selected state
    }
    
    func configureCell(trip: Trip) {
        tripDestinationLabel.text = trip.destination
    }

}
