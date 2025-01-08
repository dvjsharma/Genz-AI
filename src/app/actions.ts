'use server'

export async function processInstagramData(username: string) {
  // This would connect to your database and process the Instagram data
  console.log('Processing data for:', username)
  const response = await fetch('http://127.0.0.1:5000/process_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      instagram_id: username,
    }),
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.status} ${response.statusText}`);
  }
  const data = await response.json();
  return data;
}

export async function getChatResponse(message: string, instagramData?: any) {
  // This would connect to your AI service to get responses
    // Define the body of the POST request
    const body = {
      query: message
    };

    // Send a POST request
    const response = await fetch('http://127.0.0.1:5000/process_query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    // Check if the response is OK
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse the response as JSON
    const data = await response.json();

    // Return the response
    return {
      response: data.message || "No response received",
      data: data
    };
}

