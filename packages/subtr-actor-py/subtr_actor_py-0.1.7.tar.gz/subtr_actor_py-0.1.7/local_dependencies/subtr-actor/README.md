[![Workflow Status](https://github.com/rlrml/subtr-actor/workflows/main/badge.svg)](https://github.com/rlrml/subtr-actor/actions?query=workflow%3A%22main%22) [![](https://docs.rs/subtr-actor/badge.svg)](https://docs.rs/subtr-actor) [![Version](https://img.shields.io/crates/v/subtr-actor.svg?style=flat-square)](https://crates.io/crates/subtr-actor) ![Maintenance](https://img.shields.io/badge/maintenance-activly--developed-brightgreen.svg)
# subtr-actor

## subtr-actor

[`subtr-actor`][1] is a versatile library designed to facilitate the
processes of working with and extracting data from Rocket League replays.
Utilizing the powerful [`boxcars`][2] library for parsing, subtr-actor
simplifies (or 'subtracts', as hinted by its name) the underlying
actor-based structure of replay files, making them more accessible and
easier to manipulate.

### Overview of Key Components

- **[`ReplayProcessor`][3]**: This struct is at the heart of subtr-actor's
replay processing capabilities. In its main entry point,
[`ReplayProcessor::process`][4], it pushes network frames from the
[`boxcars::Replay`][5] that it is initialized with though an
[`ActorStateModeler`][6] instance, calling the [`Collector`][7] instance that is
provided as an argument as it does so. The [`Collector`][7] is provided with a
reference to the [`ReplayProcessor`][3] each time the it is invoked, which
allows it to use the suite of helper methods which greatly assist in the
navigation of the actor graph and the retrieval of information about the current
game state.

- **[`Collector`][7]**: This trait outlines the blueprint for data collection
from replays. The [`Collector`][7] interfaces with a [`ReplayProcessor`][3],
handling frame data and guiding the pace of replay progression with
[`TimeAdvance`][8]. It is typically invoked repeatedly through the
[`ReplayProcessor::process`][4] method as the replay is processed frame by
frame.

- **[`FrameRateDecorator`][9]**: This struct decorates a [`Collector`][7]
implementation with a target frame duration, controlling the frame rate of
the replay processing.

#### Collector implementations

[`subtr-actor`][1] also includes implementations of the [`Collector`][7] trait:

- **[`NDArrayCollector`][10]**: This [`Collector`][7] implementations translates
frame-based replay data into a 2 dimensional array in the form of a
[`::ndarray::Array2`][11] instance. The exact data that is recorded in each
frame can be configured with the [`FeatureAdder`][12] and [`PlayerFeatureAdder`][13]
instances that are provided to its constructor ([`NDArrayCollector::new`][14]).
Extending the exact behavior of [`NDArrayCollector`][10] is thus possible with
user defined [`FeatureAdder`][12] and [`PlayerFeatureAdder`][13], which is made easy
with the [`build_global_feature_adder!`][15] and [`build_player_feature_adder!`][16]
macros. The [`::ndarray::Array2`][11] produced by [`NDArrayCollector`][10] is ideal
for use with machine learning libraries like pytorch and tensorflow.

- **[`ReplayDataCollector`][17]**: This [`Collector`][7] implementation provides
an easy way to get a serializable to e.g. json (though [`serde::Serialize`][18])
representation of the replay. The representation differs from what you might get
from e.g. raw [`boxcars`][2] in that it is not a complicated graph of actor
objects, but instead something more natural where the data associated with each
entity in the game is grouped together.

### Examples

#### Getting JSON

```rust
fn get_json(filepath: std::path::PathBuf) -> anyhow::Result<String> {
    let data = std::fs::read(filepath.as_path())?;
    let replay = boxcars::ParserBuilder::new(&data)
        .must_parse_network_data()
        .on_error_check_crc()
        .parse()?;
    Ok(subtr_actor::ReplayDataCollector::new()
        .get_replay_data(&replay)
        .map_err(|e| e.variant)?
        .as_json()?)
}
```

#### Getting a [`::ndarray::Array2`][11]

In the following example, we demonstrate how to use [`boxcars`][2],
[`NDArrayCollector`][10] and [`FrameRateDecorator`][9] to write a function that
takes a replay filepath and collections of features adders and returns a
[`ReplayMetaWithHeaders`][19] along with a [`::ndarray::Array2`][11] . The resulting
[`::ndarray::Array2`][11] would be appropriate for use in a machine learning
context. Note that [`ReplayProcessor`][3] is also used implicitly here in the
[`Collector::process_replay`][20]

```rust
use subtr_actor::*;

fn get_ndarray_with_info_from_replay_filepath(
    filepath: std::path::PathBuf,
    feature_adders: FeatureAdders<f32>,
    player_feature_adders: PlayerFeatureAdders<f32>,
    fps: Option<f32>,
) -> anyhow::Result<(ReplayMetaWithHeaders, ::ndarray::Array2<f32>)> {
    let data = std::fs::read(filepath.as_path())?;
    let replay = boxcars::ParserBuilder::new(&data)
        .must_parse_network_data()
        .on_error_check_crc()
        .parse()?;

    let mut collector = NDArrayCollector::new(feature_adders, player_feature_adders);

    FrameRateDecorator::new_from_fps(fps.unwrap_or(10.0), &mut collector)
        .process_replay(&replay)
        .map_err(|e| e.variant)?;

    Ok(collector.get_meta_and_ndarray().map_err(|e| e.variant)?)
}

fn get_ndarray_with_default_feature_adders(
    filepath: std::path::PathBuf,
) -> anyhow::Result<(ReplayMetaWithHeaders, ::ndarray::Array2<f32>)> {
    get_ndarray_with_info_from_replay_filepath(
        filepath,
        vec![
            InterpolatedBallRigidBodyNoVelocities::arc_new(0.003),
            CurrentTime::arc_new(),
        ],
        vec![
            InterpolatedPlayerRigidBodyNoVelocities::arc_new(0.003),
            PlayerBoost::arc_new(),
            PlayerAnyJump::arc_new(),
            PlayerDemolishedBy::arc_new(),
        ],
        Some(30.0),
    )
}
```

#### Using [`NDArrayCollector::from_strings`][21]

In the second function we see the use of feature adders like
[`InterpolatedPlayerRigidBodyNoVelocities`][22]. The feature adders that are
included with [`subtr_actor`][1] can all be found in the
[`crate::collector::ndarray`][23] module. It is also possible to access these
feature adders by name with strings, which can be useful when implementing
bindings for other languages since those languages may not be able to access
rust structs an instantiate them easily or at all.

```rust
pub static DEFAULT_GLOBAL_FEATURE_ADDERS: [&str; 1] = ["BallRigidBody"];

pub static DEFAULT_PLAYER_FEATURE_ADDERS: [&str; 3] =
    ["PlayerRigidBody", "PlayerBoost", "PlayerAnyJump"];

fn build_ndarray_collector(
    global_feature_adders: Option<Vec<String>>,
    player_feature_adders: Option<Vec<String>>,
) -> subtr_actor::SubtrActorResult<subtr_actor::NDArrayCollector<f32>> {
    let global_feature_adders = global_feature_adders.unwrap_or_else(|| {
        DEFAULT_GLOBAL_FEATURE_ADDERS
            .iter()
            .map(|i| i.to_string())
            .collect()
    });
    let player_feature_adders = player_feature_adders.unwrap_or_else(|| {
        DEFAULT_PLAYER_FEATURE_ADDERS
            .iter()
            .map(|i| i.to_string())
            .collect()
    });
    let global_feature_adders: Vec<&str> = global_feature_adders.iter().map(|s| &s[..]).collect();
    let player_feature_adders: Vec<&str> = player_feature_adders.iter().map(|s| &s[..]).collect();
    subtr_actor::NDArrayCollector::<f32>::from_strings(
        &global_feature_adders,
        &player_feature_adders,
    )
}
```

[1]: https://docs.rs/subtr-actor/latest/subtr_actor/
[2]: https://docs.rs/boxcars/latest/boxcars/
[3]: https://docs.rs/subtr-actor/latest/subtr_actor/processor/struct.ReplayProcessor.html
[4]: https://docs.rs/subtr-actor/latest/subtr_actor/processor/struct.ReplayProcessor.html#method.process
[5]: https://docs.rs/boxcars/latest/boxcars/struct.Replay.html
[6]: https://docs.rs/subtr-actor/latest/subtr_actor/actor_state/struct.ActorStateModeler.html
[7]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/trait.Collector.html
[8]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/decorator/struct.TimeAdvance.html
[9]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/decorator/struct.FrameRateDecorator.html
[10]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/struct.NDArrayCollector.html
[11]: https://docs.rs/ndarray/latest/ndarray/type.Array2.html
[12]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/trait.FeatureAdder.html
[13]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/trait.PlayerFeatureAdder.html
[14]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/struct.NDArrayCollector.html#method.new
[15]: https://docs.rs/subtr-actor/latest/subtr_actor/macro.build_global_feature_adder.html
[16]: https://docs.rs/subtr-actor/latest/subtr_actor/macro.build_player_feature_adder.html
[17]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/replay_data/struct.ReplayDataCollector.html
[18]: https://docs.rs/serde/latest/serde/trait.Serialize.html
[19]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/struct.ReplayMetaWithHeaders.html
[20]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/trait.Collector.html#method.process_replay
[21]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/struct.NDArrayCollector.html#method.from_strings
[22]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/struct.InterpolatedPlayerRigidBodyNoVelocities.html
[23]: https://docs.rs/subtr-actor/latest/subtr_actor/collector/ndarray/index.html
