import React, { Component } from 'react'
import { connect } from 'react-redux'
import { fetchParticipants } from '../actions'

import './Dashboard.css'

class Dashboard extends Component {
  componentDidMount () {
    this.props.fetchParticipants()
  }

  renderParticipant = participant => {
    const { inactive_before_event, pull_requests } = this.props.participants[
      participant
    ]
    return (
      <li key={participant}>
        {`${inactive_before_event ? 'Newcomer' : 'Veteran'} // `}
        <span className='name'>{participant}</span>
        {` // ${pull_requests.length} pull requests`}
      </li>
    )
  }

  render () {
    const { participants } = this.props
    if (!this.props.participants) return null
    let prCount = 0

    Object.values(participants).map(
      participant => {
        console.log(participant.pull_requests)
        participant.pull_requests = participant.pull_requests.filter(pr => pr.merged || pr.state == 'open')
        console.log(participant.pull_requests)
      }
    )
    Object.values(participants).map(
      participant => (prCount += participant.pull_requests.length)
    )
    const sortedParticipants = Object.keys(
      this.props.participants
    ).sort((first, second) => {
      return (
        participants[second].pull_requests.length -
        participants[first].pull_requests.length
      )
    })

    return (
      <div>
        <h1>TOTAL PULL REQUESTS: {prCount}</h1>
        <h3>Participants ranking:</h3>
        <table>
          {sortedParticipants.map((participant, index) => {
            return (
              <tr key={index}>
                <td>
                  {this.props.participants[participant].inactive_before_event
                    ? 'Newcomer'
                    : 'Veteran'}
                </td>
                <td className='name'><a href={"https://github.com/"+participant}>{participant}</a></td>
                <td>
                  {this.props.participants[participant].pull_requests.length}
                  {' '}
                  pull requests
                  <br/>
                  {this.props.participants[participant].pull_requests.map((pr) => {
                    console.log(pr)
                    return (
                        <span>
                          <a href={pr.html_url}>{pr.title}</a>
                          <br/>
                        </span>
                    )
                  })}
                </td>
              </tr>
            )
          })}
        </table>
      </div>
    )
  }
}

export default connect(participants => ({ participants }), {
  fetchParticipants
})(Dashboard)
