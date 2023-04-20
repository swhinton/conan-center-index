
#include <atomic>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <mutex>
#include <thread>

#include "dds/dds.hpp"
#include "HelloWorldData.hpp"

using namespace org::eclipse::cyclonedds;

int main() {
  dds::domain::DomainParticipant participant(domain::default_id());
  // No IDL, no topics.
  dds::sub::Subscriber subscriber(participant);
  dds::topic::Topic<HelloWorldData::Msg> topic(participant, "HelloWorld");
  return EXIT_SUCCESS;
}
