require 'rails_helper'

RSpec.describe 'API', type: :request do
  it 'returns the details of a user' do
    get '/api/users/1'
    expect(response).to have_http_status(200)
    expect(response.body).to include('user1')
  end

  it 'updates a user' do
    put '/api/users/1', params: { user: { name: 'updated_user1', email: 'updated_user1@example.com' } }
    expect(response).to have_http_status(200)
    expect(response.body).to include('updated_user1')
  end
end
