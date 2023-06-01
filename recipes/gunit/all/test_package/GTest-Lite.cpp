//
// Copyright (c) 2016-2017 Kris Jusiak (kris at jusiak dot net)
//
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
#include "GUnit/GTest-Lite.h"
#include "GUnit/GTest.h"  // EXPECT_TRUE

int main() {
  "should be true"_test = [] { EXPECT_TRUE(true); };

  "should not run"_test_disabled = [] { throw 0; };
}
